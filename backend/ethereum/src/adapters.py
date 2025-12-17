import logging
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import json
import asyncio

from faststream.rabbit import RabbitBroker

from redis.asyncio import Redis

from web3 import Web3
from web3.types import BlockData
from eth_account import Account
from eth_typing import HexStr

import httpx

import websockets

from src.consts import (
    GAS,
    GAS_PRICE_GWEI,
    FREE_ETH_WEI
)
from src.ports import (
    StoragePort,
    EthereumServicePort,
    BlockListenerPort
)

from src.schemas import (
    TransactionSchema,
    CompleteTransactionSchema,
    TransactionStatusEnum,
    EtherscanTransactionListResponseSchema,
    ETHWalletSchema
)

from src.configs import (
    EtherscanConfig,
    InfuraConfig,
    FaucetConfig
)


class RedisStorageAdapter(StoragePort):
    storage_key: str = "PENDING_TRANSACTIONS_HASH"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def add_transaction_hash(self, tx_hash: str) -> None:
        await self._redis.sadd(self.storage_key, tx_hash)

    async def get_all_transaction_hashes(self) -> list[str]:
        hashes = await self._redis.smembers(self.storage_key)
        return [tx_hash.decode("utf-8") for tx_hash in hashes]

    async def remove_transaction_hash(self, tx_hash: str) -> None:
        await self._redis.srem(self.storage_key, tx_hash)


class EthereumServiceAdapter(EthereumServicePort):
    def __init__(
            self,
            w3: Web3,
            etherscan_config: EtherscanConfig,
            faucet_config: FaucetConfig,
            storage: StoragePort,
    ):
        self._w3 = w3
        self._etherscan_config = etherscan_config
        self._faucet_config = faucet_config
        self._storage = storage

    def create_wallet(self, user_id: UUID) -> ETHWalletSchema:
        account = self._w3.eth.account.create()

        return ETHWalletSchema(
            user_id=user_id,
            private_key=account.key.hex(),
            address=account.address,
            created_at=datetime.now()
        )

    def import_wallet(self, user_id: UUID, private_key: str) -> ETHWalletSchema:
        account = self._w3.eth.account.from_key(private_key=private_key)
        address = account.address

        balance_wei = self._w3.eth.get_balance(address)

        url = f"{self._etherscan_config.api_base_url}&apiKey={self._etherscan_config.api_key}&address={address}"

        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()

        response = EtherscanTransactionListResponseSchema(**data)

        return ETHWalletSchema(
            user_id=user_id,
            address=address,
            private_key=private_key,
            balance=Decimal(balance_wei),
            created_at=datetime.now(),
            transactions=response.result
        )

    async def create_transaction(
            self,
            private_key: str,
            to_address: str,
            amount: Decimal,
            gas: int = GAS,
            gas_price_gwei: int = GAS_PRICE_GWEI,
            payment_order_id: UUID | None = None,
            return_order_id: UUID | None = None
    ) -> TransactionSchema:
        account = Account.from_key(private_key)
        from_address = account.address
        nonce = self._w3.eth.get_transaction_count(from_address, "pending")
        gas_price = self._w3.to_wei(gas_price_gwei, "gwei")

        tx = {
            "from": from_address,
            "to": to_address,
            "value": int(amount),
            "gas": gas,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": self._w3.eth.chain_id,
        }

        signed_tx = self._w3.eth.account.sign_transaction(tx, private_key)

        tx_hash = self._w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = self._w3.to_hex(tx_hash)

        await self._storage.add_transaction_hash(tx_hash_hex)

        schema_data = {
            "hash": tx_hash_hex,
            "from": from_address,
            "to": to_address,
            "value": Decimal(amount),
            "gas": gas,
            "gasPrice": gas_price
        }

        if payment_order_id:
            schema_data.setdefault("payment_order_id", payment_order_id)

        if return_order_id:
            schema_data.setdefault("return_order_id", return_order_id)

        return TransactionSchema(**schema_data)

    async def send_free_eth(self, to_address: str):
        return await self.create_transaction(
            private_key=self._faucet_config.wallet_private_key,
            to_address=to_address,
            amount=Decimal(FREE_ETH_WEI)
        )


class BlockListenerAdapter(BlockListenerPort):
    def __init__(
            self,
            w3: Web3,
            infura_config: InfuraConfig,
            broker: RabbitBroker,
            storage: StoragePort
    ):
        self._w3 = w3
        self._infura_config = infura_config
        self._broker = broker
        self._storage = storage
        self._logger = logging.getLogger()

    def run(self) -> asyncio.Task:
        return asyncio.create_task(self._loop())

    async def _loop(self):
        self._logger.info("Starting WebSocket block listener...")

        ws_url = f"{self._infura_config.base_ws_url}/{self._infura_config.api_key}"

        while True:
            try:
                async with websockets.connect(ws_url) as ws:
                    await ws.send(
                        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]})
                    )

                    subscription_response = await ws.recv()
                    self._logger.info(f"Connected to Websockets successfully: {subscription_response}")

                    async for message in ws:
                        try:
                            response = json.loads(message)

                            if "params" in response:
                                block_hex = response["params"]["result"]["number"]
                                block_number = int(block_hex, 16)

                                self._logger.info(f"New block received: {block_number}")

                                block = self._w3.eth.get_block(block_number, full_transactions=True)
                                await self._process_block(block)

                        except Exception as e:
                            self._logger.error(f"Error processing block message: {e}")

            except Exception as e:
                self._logger.error(f"Websocket connection lost: {e}. Reconnecting in 5s...")
                await asyncio.sleep(5)

    async def _process_block(self, block: BlockData):
        pending_hashes = await self._storage.get_all_transaction_hashes()

        self._logger.info(f"Pending hashes: {pending_hashes}")

        for tx in block["transactions"]:
            tx_hash_hex = self._w3.to_hex(tx["hash"])

            if tx_hash_hex in pending_hashes:
                receipt = self._w3.eth.get_transaction_receipt(HexStr(tx_hash_hex))
                status = TransactionStatusEnum.SUCCESSFUL if receipt["status"] else TransactionStatusEnum.FAILED

                created_at = datetime.fromtimestamp(block["timestamp"])

                event_data = CompleteTransactionSchema(
                    hash=tx_hash_hex,
                    transaction_status=status,
                    created_at=created_at
                )

                self._logger.info(f"Completed pending transaction: {event_data.model_dump()}")

                await self._broker.publish(
                    queue="ethereum.complete_transaction",
                    message=event_data.model_dump()
                )

                await self._storage.remove_transaction_hash(tx_hash_hex)

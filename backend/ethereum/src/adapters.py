import logging

import asyncio

from decimal import Decimal

from datetime import datetime

from uuid import UUID

from faststream.rabbit import RabbitBroker

from redis.asyncio import Redis

from web3 import Web3
from web3.types import BlockData
from eth_account import Account
from eth_typing import HexStr

import httpx

from src.consts import GAS, GAS_PRICE_GWEI
from src.ports import (
    StoragePort,
    EthereumServicePort,
    BlockListenerPort
)

from src.schemas import (
    TransactionSchema,
    UpdateTransactionSchema,
    TransactionStatusEnum,
    EtherscanTransactionListResponseSchema,
    ETHWalletSchema
)

from src.configs import EtherscanConfig


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
            storage: StoragePort,
    ):
        self._w3 = w3
        self._etherscan_config = etherscan_config
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
    ) -> TransactionSchema:
        account = Account.from_key(private_key)
        from_address = account.address
        nonce = self._w3.eth.get_transaction_count(from_address)
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

        return TransactionSchema(**{
            "hash": tx_hash_hex,
            "from": from_address,
            "to": to_address,
            "value": Decimal(amount),
            "gas": gas,
            "gasPrice": gas_price
        })


class BlockListenerAdapter(BlockListenerPort):
    _poll_interval: float = 20.0

    def __init__(
            self,
            w3: Web3,
            broker: RabbitBroker,
            storage: StoragePort
    ):
        self._w3 = w3
        self._broker = broker
        self._storage = storage
        self._last_block = None
        self._logger = logging.getLogger("ethereum_broker")

    def run(self) -> asyncio.Task:
        return asyncio.create_task(self._loop())

    async def _loop(self):
        self._logger.info("Starting block listener...")

        while True:
            self._logger.info("Running loop...")
            latest_block_number = self._w3.eth.block_number
            if self._last_block is None:
                self._last_block = latest_block_number

            for block_num in range(self._last_block + 1, latest_block_number + 1):
                block = self._w3.eth.get_block(block_num, full_transactions=True)
                await self._process_block(block)

            self._last_block = latest_block_number

            await asyncio.sleep(self._poll_interval)

    async def _process_block(self, block: BlockData):
        pending_hashes = await self._storage.get_all_transaction_hashes()

        self._logger.info(f"Pending hashes: {pending_hashes}")

        for tx in block["transactions"]:
            tx_hash_hex = self._w3.to_hex(tx["hash"])

            if tx_hash_hex in pending_hashes:
                receipt = self._w3.eth.get_transaction_receipt(HexStr(tx_hash_hex))
                status = TransactionStatusEnum.SUCCESSFUL if receipt["status"] else TransactionStatusEnum.FAILED

                event_data = UpdateTransactionSchema(
                    hash=tx_hash_hex,
                    transaction_status=status,
                    created_at=datetime.fromtimestamp(block["timestamp"])
                )

                self._logger.info(f"Completed pending transaction: {event_data.model_dump()}")

                await self._broker.publish(
                    queue="ethereum.complete_transaction",
                    message=event_data.model_dump()
                )

                await self._storage.remove_transaction_hash(tx_hash_hex)

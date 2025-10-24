from decimal import Decimal

from datetime import datetime

from uuid import UUID

from web3 import Web3

import httpx

from src.ports import EthereumServicePort

from src.schemas import (
    EtherscanTransactionListResponseSchema,
    ETHWalletSchema
)

from src.configs import EtherscanConfig


class EthereumServiceAdapter(EthereumServicePort):
    def __init__(self, w3: Web3, etherscan_config: EtherscanConfig):
        self._w3 = w3
        self._etherscan_config = etherscan_config

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

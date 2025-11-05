from typing import TypedDict

from decimal import Decimal

from uuid import UUID

import logging

from dishka import FromDishka
from dishka.integrations.faststream import inject

from faststream.rabbit import RabbitRouter

from src.ports import EthereumServicePort
from src.schemas import (
    TransactionSchema,
    ETHWalletSchema
)

logger = logging.getLogger("ethereum_broker")

amqp_router = RabbitRouter()


class CreateWalletData(TypedDict):
    user_id: str


@amqp_router.subscriber("rest_api.create_eth_wallet")
@amqp_router.publisher("ethereum.create_eth_wallet")
@inject
async def create_wallet_handler(
        data: CreateWalletData,
        ethereum_service: FromDishka[EthereumServicePort]
) -> ETHWalletSchema:
    logger.info(f"Received message on rest_api.create_eth_service: {data}")
    user_id = UUID(data["user_id"])
    wallet = ethereum_service.create_wallet(user_id=user_id)
    logger.info(f"Publishing message to ethereum.create_eth_service: {wallet.model_dump()}")
    return wallet


class ImportWalletData(TypedDict):
    user_id: str
    private_key: str


@amqp_router.subscriber("rest_api.import_eth_wallet")
@amqp_router.publisher("ethereum.import_eth_wallet")
@inject
async def import_wallet_handler(
        data: ImportWalletData,
        ethereum_service: FromDishka[EthereumServicePort]
) -> ETHWalletSchema:
    logger.info(f"Received message on rest_api.import_eth_service: {data}")
    user_id = UUID(data["user_id"])
    private_key = data["private_key"]
    wallet = ethereum_service.import_wallet(user_id=user_id, private_key=private_key)
    logger.info(f"Publishing message to ethereum.import_eth_service: {wallet.model_dump()}")
    return wallet.model_dump()


class CreateTransactionData(TypedDict):
    private_key: str
    to_address: str
    amount: Decimal


@amqp_router.subscriber("rest_api.create_transaction")
@amqp_router.publisher("ethereum.create_pending_transaction")
@inject
async def create_transaction_handler(
        data: CreateTransactionData,
        ethereum_service: FromDishka[EthereumServicePort]
) -> TransactionSchema:
    logger.info(f"Received message on rest_api.create_transaction: {data}")
    tx = await ethereum_service.create_transaction(
        private_key=data["private_key"],
        to_address=data["to_address"],
        amount=data["amount"]
    )
    logger.info(f"Created pending transaction: {tx.model_dump()}")
    return tx.model_dump()


class SendFreeETHData(TypedDict):
    to_address: str


@amqp_router.subscriber("rest_api.request_free_eth")
@amqp_router.publisher("ethereum.create_pending_transaction")
@inject
async def send_free_eth_handler(
        data: SendFreeETHData,
        ethereum_service: FromDishka[EthereumServicePort]
) -> TransactionSchema:
    logger.info(f"Received message on rest_api.request_free_eth: {data}")
    tx = await ethereum_service.send_free_eth(to_address=data["to_address"])
    logger.info(f"Created pending transaction: {tx.model_dump()}")
    return tx.model_dump()

import logging
from decimal import Decimal

from src.domain.enums import (
    TransactionStatusEnum,
    OrderStatusEnum
)
from src.domain.ports import SecretEncryptor
from src.domain.value_objects import (
    EntityId,
    Timestamp,
    TransactionStatus,
    TransactionHash,
    OrderStatus
)

from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.ports.gateways import (
    TransactionGateway,
    WalletGateway,
    OrderGateway
)
from src.application.ports.events import EventPublisher
from src.application.dtos.request import UpdateTransactionRequestDTO
from src.application.dtos.events import (
    CreateTransactionEventDTO,
    CompleteTransactionEventDTO,
    UpdateOrderEventDTO,
    PayOrderEventDTO,
    UpdateWalletEventDTO
)

logger = logging.getLogger(__name__)


class CompleteTransactionInteractor:
    def __init__(
            self,
            transaction_gateway: TransactionGateway,
            wallet_gateway: WalletGateway,
            order_gateway: OrderGateway,
            transaction_manager: TransactionManager,
            flusher: Flusher,
            event_publisher: EventPublisher,
            secret_encryptor: SecretEncryptor
    ) -> None:
        self._transaction_gateway = transaction_gateway
        self._wallet_gateway = wallet_gateway
        self._order_gateway = order_gateway
        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._event_publisher = event_publisher
        self._secret_encryptor = secret_encryptor

    async def __call__(self, data: UpdateTransactionRequestDTO) -> None:
        logger.info(f"Updating transactions with hash {data.hash} status to {data.transaction_status}...")

        await self._transaction_gateway.update(
            created_at=Timestamp(data.created_at).value,
            status=TransactionStatus(data.transaction_status).value,
            tx_hash=TransactionHash(data.hash).value,
        )

        await self._flusher.flush()

        transactions = await self._transaction_gateway.read(tx_hash=TransactionHash(data.hash).value)

        if len(transactions) > 0:
            logger.info("Emitting event rest_api.complete_transaction (for payer)...")

            await self._event_publisher.complete_transaction(
                CompleteTransactionEventDTO(
                    user_id=transactions[0]["wallet"]["user_id"],
                    transaction_id=transactions[0]["id"],
                    transaction_hash=transactions[0]["transaction_hash"],
                    from_address=transactions[0]["from_address"],
                    to_address=transactions[0]["to_address"],
                    value=transactions[0]["value"] / (10 ** transactions[0]["wallet"]["asset"]["decimals"]),
                    transaction_fee=transactions[0]["transaction_fee"] / (
                            10 ** transactions[0]["wallet"]["asset"]["decimals"]),
                    transaction_status=transactions[0]["transaction_status"],
                    asset_symbol=transactions[0]["wallet"]["asset"]["symbol"],
                    wallet_address=transactions[0]["wallet"]["address"],
                    created_at=transactions[0]["created_at"]
                )
            )

            if transactions[0]["transaction_status"] == TransactionStatusEnum.SUCCESSFUL:
                logger.info("Updating payer wallet balance in database...")

                await self._wallet_gateway.decrement_balance(
                    wallet_id=transactions[0]["wallet"]["id"],
                    amount=transactions[0]["transaction_fee"] + transactions[0]["value"]
                )

                await self._flusher.flush()

                wallet = await self._wallet_gateway.read(wallet_id=transactions[0]["wallet"]["id"])

                logger.info("Emitting event rest_api.update_wallet (for payer)...")

                await self._event_publisher.update_wallet(
                    UpdateWalletEventDTO(
                        user_id=wallet["user_id"],
                        wallet_id=wallet["id"],
                        balance=wallet["balance"] / (10 ** wallet["asset"]["decimals"])
                    )
                )

        if len(transactions) > 1:
            logger.info("Emitting event rest_api.complete_transaction (for receiver)...")

            await self._event_publisher.complete_transaction(
                CompleteTransactionEventDTO(
                    user_id=transactions[1]["wallet"]["user_id"],
                    transaction_id=transactions[1]["id"],
                    transaction_hash=transactions[1]["transaction_hash"],
                    from_address=transactions[1]["from_address"],
                    to_address=transactions[1]["to_address"],
                    value=transactions[1]["value"] / (10 ** transactions[1]["wallet"]["asset"]["decimals"]),
                    transaction_fee=transactions[1]["transaction_fee"] / (
                            10 ** transactions[1]["wallet"]["asset"]["decimals"]),
                    transaction_status=transactions[1]["transaction_status"],
                    asset_symbol=transactions[1]["wallet"]["asset"]["symbol"],
                    wallet_address=transactions[1]["wallet"]["address"],
                    created_at=transactions[1]["created_at"]
                )
            )

            if transactions[1]["transaction_status"] == TransactionStatusEnum.SUCCESSFUL:
                logger.info("Updating receiver wallet balance in database...")

                await self._wallet_gateway.increment_balance(
                    wallet_id=transactions[1]["wallet"]["id"],
                    amount=transactions[1]["value"]
                )

                await self._flusher.flush()

                wallet = await self._wallet_gateway.read(wallet_id=transactions[1]["wallet"]["id"])

                logger.info("Emitting event rest_api.update_wallet (for receiver)...")

                await self._event_publisher.update_wallet(
                    UpdateWalletEventDTO(
                        user_id=wallet["user_id"],
                        wallet_id=wallet["id"],
                        balance=wallet["balance"] / (10 ** wallet["asset"]["decimals"])
                    )
                )

        logger.info("Checking if received transaction is related to some order...")

        order = await self._order_gateway.read(tx_hash=TransactionHash(data.hash).value)

        if order:
            logger.info("Checking if received transaction is complete payment transaction for new order...")

            if order["status"] == OrderStatusEnum.NEW:

                if data.transaction_status == TransactionStatusEnum.SUCCESSFUL:
                    logger.info("Emitting event rest_api.pay_order...")

                    await self._event_publisher.pay_order(
                        PayOrderEventDTO(
                            user_id=order["wallet"]["user_id"],
                            order_id=order["id"],
                            transaction_hash=order["payment_transaction"]["transaction_hash"]
                        )
                    )

                if data.transaction_status == TransactionStatusEnum.FAILED:
                    logger.info(f"Updating order status to {data.transaction_status}...")

                    await self._order_gateway.update(
                        order_id=EntityId(order["id"]).value,
                        status=OrderStatus(OrderStatusEnum.FAILED).value
                    )

                    logger.info("Emitting event rest_api.update_order...")

                    await self._event_publisher.update_order(
                        UpdateOrderEventDTO(
                            user_id=order["wallet"]["user_id"],
                            order_id=order["id"],
                            status=OrderStatusEnum.FAILED
                        )
                    )

                    logger.info("Emitting rest_api.create_transaction...")

                    await self._event_publisher.create_transaction(
                        CreateTransactionEventDTO(
                            # from product seller
                            private_key=self._secret_encryptor.decrypt(
                                order["product"]["wallet"]["encrypted_private_key"]),
                            # to customer
                            to_address=order["wallet"]["address"],
                            amount=order["product"]["price"] - Decimal("1.5") * order["payment_transaction"][
                                "transaction_fee"],
                            return_order_id=order["id"]
                        )
                    )

            await self._flusher.flush()

        await self._transaction_manager.commit()

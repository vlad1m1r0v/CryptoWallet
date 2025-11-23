import logging

from src.domain.value_objects import (
    EntityId,
    TransactionHash,
    TransactionStatus,
    TransactionFee,
    TransactionValue,
    Address
)
from src.domain.entities import Transaction
from src.domain.services import TransactionService

from src.application.ports.transaction import (
    TransactionManager,
    Flusher
)
from src.application.ports.gateways import (
    WalletGateway,
    TransactionGateway,
    OrderGateway
)
from src.application.ports.events import EventPublisher
from src.application.dtos.request import CreatePendingTransactionRequestDTO
from src.application.dtos.events import (
    SavePendingTransactionEventDTO,
    UpdateOrderEventDTO
)

logger = logging.getLogger(__name__)


class CreatePendingTransactionInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
            order_gateway: OrderGateway,
            transaction_service: TransactionService,
            transaction_manager: TransactionManager,
            flusher: Flusher,
            event_publisher: EventPublisher
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway
        self._order_gateway = order_gateway
        self._transaction_service = transaction_service
        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._event_publisher = event_publisher

    async def __call__(self, data: CreatePendingTransactionRequestDTO) -> None:
        transactions_to_create: list[Transaction] = []

        logger.info("Checking if transaction is sent from one of existing wallets from database...")

        from_wallet = await self._wallet_gateway.read(address=data.from_address)

        if from_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=EntityId(from_wallet["id"]),
                transaction_hash=TransactionHash(data.hash),
                from_address=Address(data.from_address),
                to_address=Address(data.to_address),
                value=TransactionValue(data.value),
                transaction_status=TransactionStatus(data.transaction_status),
                transaction_fee=TransactionFee(data.transaction_fee),
            )

            transactions_to_create.append(transaction)

        logger.info("Checking if transaction is sent to one of existing wallets from database...")

        to_wallet = await self._wallet_gateway.read(address=data.to_address)

        if to_wallet:
            transaction = self._transaction_service.create_transaction(
                wallet_id=EntityId(to_wallet["id"]),
                transaction_hash=TransactionHash(data.hash),
                from_address=Address(data.from_address),
                to_address=Address(data.to_address),
                value=TransactionValue(data.value),
                transaction_status=TransactionStatus(data.transaction_status),
                transaction_fee=TransactionFee(data.transaction_fee),
            )

            transactions_to_create.append(transaction)

        logger.info("Inserting new transactions into database...")

        self._transaction_gateway.add(transactions=transactions_to_create)

        await self._flusher.flush()

        transactions = await self._transaction_gateway.read(tx_hash=data.hash)

        if len(transactions) > 0:
            logger.info("Emitting event rest_api.create_pending_transaction (for payer)...")

            await self._event_publisher.save_pending_transaction(
                SavePendingTransactionEventDTO(
                    user_id=transactions[0]["wallet"]["user_id"],
                    transaction_id=transactions[0]["id"],
                    transaction_hash=transactions[0]["transaction_hash"],
                    from_address=transactions[0]["from_address"],
                    to_address=transactions[0]["to_address"],
                    value=transactions[0]["value"] / (10 ** transactions[0]["wallet"]["asset"]["decimals"]),
                    transaction_fee=transactions[0]["transaction_fee"] / (
                            10 ** transactions[0]["wallet"]["asset"]["decimals"]),
                    transaction_status=transactions[0]["transaction_status"],
                    asset_symbol=transactions[0]["wallet"]["asset"]["symbol"]
                )
            )

        if len(transactions) > 1:
            logger.info("Emitting event rest_api.create_pending_transaction (for receiver)...")

            await self._event_publisher.save_pending_transaction(
                SavePendingTransactionEventDTO(
                    user_id=transactions[1]["wallet"]["user_id"],
                    transaction_id=transactions[1]["id"],
                    transaction_hash=transactions[1]["transaction_hash"],
                    from_address=transactions[1]["from_address"],
                    to_address=transactions[1]["to_address"],
                    value=transactions[1]["value"] / (10 ** transactions[1]["wallet"]["asset"]["decimals"]),
                    transaction_fee=transactions[1]["transaction_fee"] / (
                            10 ** transactions[1]["wallet"]["asset"]["decimals"]),
                    transaction_status=transactions[1]["transaction_status"],
                    asset_symbol=transactions[1]["wallet"]["asset"]["symbol"]
                )
            )

        logger.info("Checking if incoming transaction is payment order transaction...")

        if data.payment_order_id:
            logger.info("Update field 'payment_order_id' for order...")

            await self._order_gateway.update(
                order_id=data.payment_order_id,
                payment_transaction_id=transactions[0].id_.value
            )

            await self._flusher.flush()

            logger.info("Emitting event rest_api.update_order...")

            order = await self._order_gateway.read(tx_hash=data.hash)

            await self._event_publisher.update_order(
                UpdateOrderEventDTO(
                    user_id=order["wallet"]["user_id"],
                    order_id=order["id"],
                    payment_transaction_hash=order["payment_transaction"]["transaction_hash"]
                ))

        if data.return_order_id:
            logger.info("Update field 'return_order_id' for order...")

            await self._order_gateway.update(
                order_id=data.return_order_id,
                return_transaction_id=transactions[0].id_.value
            )

            await self._flusher.flush()

            logger.info("Emitting event rest_api.update_order...")

            order = await self._order_gateway.read(tx_hash=data.hash)

            await self._event_publisher.update_order(
                UpdateOrderEventDTO(
                    user_id=order["wallet"]["user_id"],
                    order_id=order["id"],
                    return_transaction_hash=order["return_transaction"]["transaction_hash"]
                )
            )

        await self._transaction_manager.commit()

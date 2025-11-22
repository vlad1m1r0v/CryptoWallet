from decimal import Decimal
from uuid import UUID
import logging

from src.domain.enums import OrderStatusEnum
from src.domain.ports import SecretEncryptor
from src.domain.value_objects import (
    EntityId,
    OrderStatus
)

from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import OrderGateway
from src.application.ports.events import EventPublisher
from src.application.dtos.events import (
    CreateTransactionEventDTO,
    UpdateOrderEventDTO
)

logger = logging.getLogger(__name__)


class UpdateOrderInteractor:
    def __init__(
            self,
            order_gateway: OrderGateway,
            event_publisher: EventPublisher,
            transaction_manager: TransactionManager,
            secret_encryptor: SecretEncryptor
    ):
        self._order_gateway = order_gateway
        self._event_publisher = event_publisher
        self._transaction_manager = transaction_manager
        self._secret_encryptor = secret_encryptor

    async def __call__(self, order_id: UUID, status: OrderStatusEnum) -> None:
        order_id = EntityId(order_id)
        status = OrderStatus(status)

        logger.info("Updating order status in database...")

        await self._order_gateway.update(
            order_id=order_id.value,
            status=status.value
        )
        await self._transaction_manager.commit()

        if status.value in [
            OrderStatusEnum.FAILED,
            OrderStatusEnum.RETURNED
        ]:
            logger.info(f"Order status is {status.value}. Returning money to customer...")

            order = await self._order_gateway.read(order_id=order_id.value)

            await self._event_publisher.create_transaction(
                CreateTransactionEventDTO(
                    # from product seller
                    private_key=self._secret_encryptor.decrypt(order["product"]["wallet"]["encrypted_private_key"]),
                    # to customer
                    to_address=order["wallet"]["address"],
                    amount=order["product"]["price"] - Decimal("1.5") * order["payment_transaction"]["transaction_fee"],
                    return_order_id=order["id"]
                )
            )

        logger.info("Emitting event rest_api.update_order...")

        await self._event_publisher.update_order(
            UpdateOrderEventDTO(
                order_id=order_id.value,
                status=status.value
            )
        )

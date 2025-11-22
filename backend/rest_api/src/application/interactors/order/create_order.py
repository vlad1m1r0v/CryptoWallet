from uuid import UUID
import logging

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException,
    ProductNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    Address
)
from src.domain.services import OrderService
from src.domain.ports import SecretEncryptor

from src.application.ports.gateways import (
    WalletGateway,
    ProductGateway,
    OrderGateway
)
from src.application.ports.transaction import TransactionManager
from src.application.ports.events import EventPublisher
from src.application.dtos.request import CreateOrderRequestDTO
from src.application.dtos.response import OrderResponseDTO
from src.application.dtos.events import (
    CreateOrderEventDTO,
    CreateTransactionEventDTO
)

logger = logging.getLogger(__name__)


class CreateOrderInteractor:
    def __init__(
            self,
            order_service: OrderService,
            order_gateway: OrderGateway,
            wallet_gateway: WalletGateway,
            product_gateway: ProductGateway,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher,
            secret_encryptor: SecretEncryptor
    ):
        self._order_service = order_service
        self._order_gateway = order_gateway
        self._wallet_gateway = wallet_gateway
        self._product_gateway = product_gateway
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher
        self._secret_encryptor = secret_encryptor

    async def __call__(self, user_id: UUID, data: CreateOrderRequestDTO) -> OrderResponseDTO:
        product_id = EntityId(data.product_id)
        wallet_id = EntityId(data.wallet_id)
        user_id = EntityId(user_id)

        logger.info("Checking if product with given id exists...")

        product = await self._product_gateway.read(product_id=product_id.value)

        if not product:
            raise ProductNotFoundException()

        logger.info("Checking if wallet with given id exists...")

        wallet = await self._wallet_gateway.read(wallet_id=wallet_id.value)

        if not wallet:
            raise WalletNotFoundException()

        logger.info("Checking if user is the owner of wallet...")

        if wallet["user_id"] != user_id.value:
            raise UserIsNotOwnerOfWalletException(user_id, Address(wallet["address"]))

        logger.info("Inserting new order record into database...")

        entity = self._order_service.create_order(
            wallet_id=wallet_id,
            product_id=product_id
        )

        self._order_gateway.add(entity)

        await self._transaction_manager.commit()

        order = await self._order_gateway.read(order_id=entity.id_.value)

        logger.info("Emitting event rest_api.create_transaction...")

        await self._event_publisher.create_transaction(
            CreateTransactionEventDTO(
                private_key=self._secret_encryptor.decrypt(wallet["encrypted_private_key"]),
                to_address=order["product"]["wallet"]["address"],
                amount=order["product"]["price"],
                payment_order_id=order["id"]
            )
        )

        logger.info("Emitting event rest_api.create_order...")

        await self._event_publisher.create_order(
            CreateOrderEventDTO(
                order_id=order["id"],
                status=order["status"],
                created_at=order["created_at"]
            )
        )

        return order

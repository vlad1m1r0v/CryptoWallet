from uuid import UUID

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException,
    ProductNotFoundException
)
from src.domain.value_objects import EntityId
from src.domain.services import OrderService
from src.domain.ports import SecretEncryptor

from src.application.dtos.request import CreateOrderRequestDTO
from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import (
    WalletGateway,
    ProductGateway,
    OrderGateway
)
from src.application.ports.transaction import TransactionManager
from src.application.ports.events import EventPublisher


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

        product = await self._product_gateway.read_by_id(product_id)

        if not product:
            raise ProductNotFoundException()

        wallet = await self._wallet_gateway.read_by_id(wallet_id)

        if not wallet:
            raise WalletNotFoundException()

        if wallet.user_id != user_id:
            raise UserIsNotOwnerOfWalletException(user_id, wallet.address)

        entity = self._order_service.create_order(
            wallet_id=wallet_id,
            product_id=product_id
        )

        self._order_gateway.add(entity)

        await self._transaction_manager.commit()

        order = await self._order_gateway.get_order(order_id=entity.id_)

        await self._event_publisher.create_transaction(
            private_key=self._secret_encryptor.decrypt(wallet.encrypted_private_key).value,
            to_address=order["product"]["wallet"]["address"],
            amount=order["product"]["price"],
            payment_order_id=order["id"]
        )

        await self._event_publisher.create_order(
            order_id=order["id"],
            status=order["status"],
            created_at=order["created_at"]
        )

        return order

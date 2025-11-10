from uuid import UUID

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException,
    ProductNotFoundException
)
from src.domain.value_objects import EntityId
from src.domain.services import OrderService

from src.application.dtos.request import CreateOrderRequestDTO
from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import (
    WalletGateway,
    ProductGateway,
    OrderGateway
)
from src.application.ports.transaction import TransactionManager


class CreateOrderInteractor:
    def __init__(
            self,
            order_service: OrderService,
            order_gateway: OrderGateway,
            wallet_gateway: WalletGateway,
            product_gateway: ProductGateway,
            transaction_manager: TransactionManager
    ):
        self._order_service = order_service
        self._order_gateway = order_gateway
        self._wallet_gateway = wallet_gateway
        self._product_gateway = product_gateway
        self._transaction_manager = transaction_manager

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

        return await self._order_gateway.get_order(order_id=entity.id_)

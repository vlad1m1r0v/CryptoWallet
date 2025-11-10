from uuid import UUID

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    ProductName,
    ProductPrice,
    UploadedFile,
    Filename
)
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
        ...

from uuid import UUID

from src.domain.value_objects import EntityId

from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import OrderGateway


class GetOrdersInteractor:
    def __init__(self, order_gateway: OrderGateway):
        self._order_gateway = order_gateway

    async def __call__(self, user_id: UUID) -> list[OrderResponseDTO]:
        user_id = EntityId(user_id)
        return await self._order_gateway.get_orders(user_id)

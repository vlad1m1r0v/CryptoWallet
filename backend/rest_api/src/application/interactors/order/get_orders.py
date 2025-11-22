from uuid import UUID
import logging

from src.domain.value_objects import EntityId

from src.application.dtos.response import OrderResponseDTO
from src.application.ports.gateways import OrderGateway

logger = logging.getLogger(__name__)

class GetOrdersInteractor:
    def __init__(self, order_gateway: OrderGateway):
        self._order_gateway = order_gateway

    async def __call__(self, user_id: UUID) -> list[OrderResponseDTO]:
        user_id = EntityId(user_id)

        logger.info(f"Getting list of orders for user from database...")

        return await self._order_gateway.list(user_id=user_id.value)

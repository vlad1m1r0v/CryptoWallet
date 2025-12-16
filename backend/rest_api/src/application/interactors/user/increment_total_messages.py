from uuid import UUID
import logging

from src.application.ports.gateways import UserGateway
from src.application.ports.transaction import TransactionManager

logger = logging.getLogger(__name__)


class IncrementTotalMessagesInteractor:
    def __init__(
            self,
            user_gateway: UserGateway,
            transaction_manager: TransactionManager,
    ):
        self._user_gateway = user_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID) -> None:
        logger.info(f"Incrementing total messages for user {user_id}...")
        await self._user_gateway.increment_total_messages(user_id=user_id)
        await self._transaction_manager.commit()

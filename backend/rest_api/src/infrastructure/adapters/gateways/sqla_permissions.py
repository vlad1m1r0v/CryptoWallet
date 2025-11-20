from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Permissions

from src.application.ports.gateways import PermissionsGateway

from src.infrastructure.persistence.database.mappers import PermissionsMapper
from src.infrastructure.persistence.database.models import Permissions as PermissionsM


class SqlaPermissionsGateway(PermissionsGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, entity: Permissions) -> None:
        model = PermissionsMapper.to_model(entity)
        self._session.add(model)

    async def update(self, user_id: UUID, has_chat_access: bool = True) -> None:
        stmt = (
            update(PermissionsM)
            .where(PermissionsM.user_id == user_id)
            .values(has_chat_access=has_chat_access)
        )

        await self._session.execute(stmt)

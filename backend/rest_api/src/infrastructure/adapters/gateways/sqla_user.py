from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User as UserE
from src.application.ports.gateways.user import UserGateway
from src.domain.value_objects.email import Email
from src.domain.value_objects.entity_id import EntityId
from src.infrastructure.persistence.database.models.user import User as UserM
from src.infrastructure.persistence.database.mappers.user import UserMapper


class SqlaUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, user: UserE) -> UserE:
        model = UserMapper.to_model(user)
        self._session.add(model)
        return user

    async def update(self, user: UserE) -> UserE:
        stmt = (
            update(UserM)
            .where(UserM.id == user.id_.value)
            .values(
                username=user.username.value,
                password_hash=user.password_hash.value,
            )
            .returning(UserM)
        )

        result = await self._session.execute(stmt)
        updated_model = result.scalar_one()

        return UserMapper.to_entity(updated_model)

    async def read_by_id(self, user_id: EntityId) -> UserE | None:
        stmt = select(UserM).where(UserM.id == user_id.value)
        result = await self._session.execute(stmt)
        model: UserM | None = result.scalar_one_or_none()
        if not model:
            return None
        return UserMapper.to_entity(model)

    async def read_by_email(self, email: Email) -> UserE | None:
        stmt = select(UserM).where(UserM.email == email.value)
        result = await self._session.execute(stmt)
        model: UserM | None = result.scalar_one_or_none()
        if not model:
            return None
        return UserMapper.to_entity(model)

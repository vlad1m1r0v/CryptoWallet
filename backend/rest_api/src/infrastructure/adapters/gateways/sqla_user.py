from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities import User as UserE
from src.domain.value_objects import (
    Email,
    EntityId
)

from src.application.ports.gateways import UserGateway
from src.application.dtos.response.user import GetUserProfileResponseDTO

from src.infrastructure.persistence.database.models import User as UserM
from src.infrastructure.persistence.database.mappers import (
    UserMapper,
    ProfileMapper
)


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
                avatar_filename=user.avatar_filename.value,
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

    async def get_user_profile(self, user_id: EntityId) -> GetUserProfileResponseDTO | None:
        stmt = (
            select(UserM)
            .options(selectinload(UserM.wallets))
            .where(UserM.id == user_id.value)
        )

        result = await self._session.execute(stmt)
        model: UserM | None = result.scalar_one_or_none()
        if not model:
            return None
        return ProfileMapper.to_dto(model)

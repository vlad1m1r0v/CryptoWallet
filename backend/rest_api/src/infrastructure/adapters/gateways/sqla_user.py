from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.domain.entities import User

from src.application.ports.gateways import UserGateway
from src.application.dtos.response import UserResponseDTO

from src.infrastructure.persistence.database.models import User as UserM
from src.infrastructure.persistence.database.mappers import UserMapper


class SqlaUserGateway(UserGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, user: User) -> None:
        model = UserMapper.to_model(user)
        self._session.add(model)

    async def update(
            self,
            user_id: UUID,
            username: Optional[str] = None,
            password_hash: Optional[bytes] = None,
            avatar_filename: Optional[str] = None,
    ) -> None:
        values_to_update = {}

        if username is not None:
            values_to_update["username"] = username

        if password_hash is not None:
            values_to_update["password_hash"] = password_hash

        if avatar_filename is not None:
            values_to_update["avatar_filename"] = avatar_filename

        if not values_to_update:
            return

        stmt = (
            update(UserM)
            .where(UserM.id == user_id)
            .values(**values_to_update)
        )

        await self._session.execute(stmt)

    async def read(
            self,
            user_id: Optional[UUID] = None,
            email: Optional[str] = None
    ) -> UserResponseDTO | None:
        stmt: Select = (select(UserM)
        .options(
            joinedload(UserM.permissions),
            selectinload(UserM.wallets))
        )

        if user_id:
            stmt = stmt.where(UserM.id == user_id)

        elif email:
            stmt = stmt.where(UserM.email == email)

        else:
            return None

        result = await self._session.execute(stmt)
        model: UserM | None = result.scalar_one_or_none()

        if not model:
            return None

        return UserMapper.to_dto(model)

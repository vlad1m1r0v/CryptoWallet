from typing import NewType
from uuid import UUID

from abc import ABC, abstractmethod

from pymongo.asynchronous.collection import AsyncCollection

from mongo.dtos import (
    CreateUserDTO,
    UpdateUserDTO
)

UserCollection = NewType("UserCollection", AsyncCollection)
MessageCollection = NewType("MessageCollection", AsyncCollection)


class UserRepository(ABC):
    @abstractmethod
    async def create(self, dto: CreateUserDTO) -> None:
        ...

    @abstractmethod
    async def update(self, dto: UpdateUserDTO) -> None:
        ...

    @abstractmethod
    async def delete_avatar(self, user_id: UUID) -> None:
        ...


class MongoUserRepository(UserRepository):
    def __init__(self, user_collection: UserCollection) -> None:
        self._collection = user_collection

    async def create(self, dto: CreateUserDTO) -> None:
        doc = {
            "_id": str(dto.user_id),
            "username": dto.username,
            "avatar_filename": None
        }

        await self._collection.insert_one(doc)

    async def update(self, dto: UpdateUserDTO) -> None:
        update_data = {}

        if dto.username:
            update_data["username"] = dto.username

        if dto.avatar_filename:
            update_data["avatar_filename"] = dto.avatar_filename

        if update_data:
            await self._collection.update_one(
                {"_id": str(dto.user_id)},
                {"$set": update_data}
            )

    async def delete_avatar(self, user_id: UUID) -> None:
        await self._collection.update_one(
            {"_id": str(user_id)},
            {"$set": {"avatar_filename": None}}
        )

from typing import NewType
from uuid import UUID

from abc import ABC, abstractmethod

from pymongo.asynchronous.collection import AsyncCollection

from mongo.dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserDTO
)

from configs import config

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

    @abstractmethod
    async def get_user(self, user_id: UUID) -> UserDTO:
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

    async def get_user(self, user_id: UUID) -> UserDTO | None:
        user = await self._collection.find_one({"_id": str(user_id)})

        if not user:
            return None

        return UserDTO(
            id=str(user["_id"]),
            username=user["username"],
            avatar_url=f"{config.s3.base_file_url}/{user['avatar_filename']}" if user["avatar_filename"] else None
        )

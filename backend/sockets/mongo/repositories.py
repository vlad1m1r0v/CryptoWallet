from typing import NewType
from uuid import UUID, uuid4
from datetime import datetime, UTC
from abc import ABC, abstractmethod

from pymongo import ASCENDING
from pymongo.asynchronous.collection import AsyncCollection

from mongo.dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserDTO,
    CreateMessageDTO,
    MessageDTO
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


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, dto: CreateMessageDTO) -> None:
        ...

    @abstractmethod
    async def list(self) -> list[MessageDTO]:
        ...


class MongoMessageRepository(MessageRepository):
    def __init__(self, message_collection: MessageCollection) -> None:
        self._collection = message_collection

    async def create(self, dto: CreateMessageDTO) -> MessageDTO:
        new_message_id = str(uuid4())
        created_time = datetime.now(UTC)

        doc = {
            "_id": new_message_id,
            "user_id": str(dto.user_id),
            "text": dto.text,
            "image_filename": dto.image,
            "created_at": created_time
        }

        await self._collection.insert_one(doc)

        pipeline = [
            {"$match": {"_id": new_message_id}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},

            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "text": "$text",
                    "created_at": "$created_at",
                    "image_url": {
                        "$cond": {
                            "if": "$image_filename",
                            "then": {"$concat": [config.s3.base_file_url, "/", "$image_filename"]},
                            "else": None
                        }
                    },
                    "user": {
                        "id": "$user._id",
                        "username": "$user.username",
                        "avatar_url": {
                            "$cond": {
                                "if": "$user.avatar_filename",
                                "then": {"$concat": [config.s3.base_file_url, "/", "$user.avatar_filename"]},
                                "else": None
                            }
                        }
                    }
                }
            }
        ]

        cursor = await self._collection.aggregate(pipeline)

        result = await cursor.next()



        return MessageDTO(**{**result, "created_at": str(result["created_at"])})

    async def list(self) -> list[MessageDTO]:
        LIMIT = 10

        pipeline = [
            {"$sort": {"created_at": ASCENDING}},
            {"$limit": LIMIT},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 0,
                    "id": "$_id",
                    "text": "$text",
                    "created_at": "$created_at",
                    "image_url": {
                        "$cond": {
                            "if": "$image_filename",
                            "then": {"$concat": [config.s3.base_file_url, "/", "$image_filename"]},
                            "else": None
                        }
                    },
                    "user": {
                        "id": "$user._id",
                        "username": "$user.username",
                        "avatar_url": {
                            "$cond": {
                                "if": "$user.avatar_filename",
                                "then": {"$concat": [config.s3.base_file_url, "/", "$user.avatar_filename"]},
                                "else": None
                            }
                        }
                    }
                }
            }
        ]

        cursor = await self._collection.aggregate(pipeline)

        result_list = await cursor.to_list(length=LIMIT)

        return [
            MessageDTO(**{**item, "created_at": str(item["created_at"])})
            for item in result_list
        ]

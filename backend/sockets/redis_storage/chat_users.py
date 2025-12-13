from abc import ABC, abstractmethod
import json

from redis.asyncio import Redis

from mongo.dtos import UserDTO


class ChatUsersStorage(ABC):
    @abstractmethod
    async def add_session(self, user: UserDTO, sid: str) -> None:
        ...

    @abstractmethod
    async def remove_session(self, user_id: str, sid: str) -> bool:
        ...

    @abstractmethod
    async def list_users(self) -> list[UserDTO]:
        ...


class RedisChatUsersStorage(ChatUsersStorage):
    USERS_METADATA_KEY: str = "CONNECTED_USERS_META"

    USER_SESSIONS_PREFIX: str = "USER_SESSIONS:"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def add_session(self, user: UserDTO, sid: str) -> None:
        user_id_str = str(user["id"])

        session_key = f"{self.USER_SESSIONS_PREFIX}{user_id_str}"
        await self._redis.sadd(session_key, sid)

        user_json = json.dumps({
            "id": user_id_str,
            "username": user["username"],
            "avatar_url": user["avatar_url"]
        })

        await self._redis.hset(self.USERS_METADATA_KEY, user_id_str, user_json)

    async def remove_session(self, user_id: str, sid: str) -> bool:
        session_key = f"{self.USER_SESSIONS_PREFIX}{user_id}"

        await self._redis.srem(session_key, sid)

        remaining_sessions = await self._redis.scard(session_key)

        if remaining_sessions == 0:
            await self._redis.hdel(self.USERS_METADATA_KEY, user_id)
            return True

        return False

    async def list_users(self) -> list[UserDTO]:
        raw_items = await self._redis.hgetall(self.USERS_METADATA_KEY)

        users: list[UserDTO] = []

        for raw in raw_items.values():
            data = json.loads(raw)
            users.append(data)

        return users

import logging
from uuid import UUID

import socketio

from dishka import make_async_container, Scope

from utilities.file import base64_to_file

from ws.types import Message

from jwt_decoder import JwtDecoder

from mongo.dtos import CreateMessageDTO
from mongo.repositories import (
    UserRepository,
    MessageRepository
)

from redis_storage import ChatUsersStorage

from s3 import FileUploader

from ioc.registry import get_providers

from configs import Config, config

container = make_async_container(*get_providers(), context={Config: config})

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class ChatNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        async with container(scope=Scope.REQUEST) as nested_container:
            decoder = await nested_container.get(JwtDecoder)
            users_repository = await nested_container.get(UserRepository)
            message_repository = await nested_container.get(MessageRepository)
            chat_users_storage = await nested_container.get(ChatUsersStorage)

            if not (token := auth.get("token") if auth else None): return False

            try:
                payload = decoder.decode(token)
            except Exception:
                return False

            if not (user_id := payload.get("user_id")): return False

            user = await users_repository.get_user(UUID(user_id))

            if not (user := await users_repository.get_user(UUID(user_id))): return False

            await self.save_session(sid, {"user_id": user_id})

            was_user_connected = user_id in [u['id'] for u in await chat_users_storage.list_users()]

            await chat_users_storage.add_session(user, sid)

            connected_users = await chat_users_storage.list_users()
            await self.emit("list_users", data=connected_users, to=sid)

            messages = await message_repository.list()
            await self.emit("list_messages", data=messages, to=sid)

            if not was_user_connected:
                await self.emit("join_chat", data=user, skip_sid=sid)

            logger.info(f"[Chat namespace]: User {user_id} connected: {sid}.")
            return True

    async def on_create_message(self, sid, data: Message):
        session = await self.get_session(sid)
        user_id = session.get("user_id")
        logger.info(f"[Chat namespace]: User {user_id} sent message.")

        async with container(scope=Scope.REQUEST) as nested_container:
            file_uploader = await nested_container.get(FileUploader)
            message_repository = await nested_container.get(MessageRepository)

            fields = {}

            fields.setdefault("user_id", data["user_id"])
            fields.setdefault("text", data["text"])

            if image_base64 := data.get("image", None):
                image_file = base64_to_file(image_base64)
                image_url = file_uploader.upload_image(image_file)
                fields.setdefault("image", image_url)

            message = await message_repository.create(CreateMessageDTO(**fields))
            await self.emit("send_message", data=message)



    async def on_disconnect(self, sid, reason):
        session = await self.get_session(sid)

        if not (user_id := session.get("user_id")):
            logger.info(f"[Chat namespace]: Disconnected unauthenticated: {sid}")
            return

        async with container(scope=Scope.REQUEST) as nested_container:
            chat_users_storage = await nested_container.get(ChatUsersStorage)

            is_last_session = await chat_users_storage.remove_session(user_id, sid)

            if is_last_session:
                await self.emit("leave_chat", data={"id": user_id}, skip_sid=sid)

            logger.info(
                f"[Chat namespace]: Disconnected: {sid}. User {user_id}. Reason: {reason}. Last session: {is_last_session}."
            )

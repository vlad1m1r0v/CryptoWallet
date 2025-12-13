import logging

import socketio

from dishka import make_async_container, Scope

from jwt_decoder import JwtDecoder

from ioc.registry import get_providers

from configs import Config, config

container = make_async_container(*get_providers(), context={Config: config})

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class DefaultNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        async with container(scope=Scope.REQUEST) as nested_container:

            decoder = await nested_container.get(JwtDecoder)

            if not (token := auth.get("token") if auth else None):
                return False

            try:
                payload = decoder.decode(token)
            except Exception:
                return False

            if not (user_id := payload.get("user_id")):
                return False

            await self.save_session(sid, {"user_id": user_id})
            await self.enter_room(sid, f"user:{user_id}")

            logger.info(f"[Default namespace]: User {user_id} connected: {sid}")
            return True

    async def on_disconnect(self, sid, reason):
        session = await self.get_session(sid)
        logger.info(f"[Default namespace]: Disconnected: {sid}. Session: {session}")
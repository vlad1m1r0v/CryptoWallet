import logging

import socketio

from aiohttp import web

from dishka import make_async_container, Scope

from jwt_decoder import JwtDecoder

from ioc.registry import get_providers

from configs import (
    config,
    Config
)

container = make_async_container(*get_providers(), context={Config: config})

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

sio = socketio.AsyncServer(
    async_mode='aiohttp',
    client_manager=socketio.AsyncRedisManager(config.redis.url),
    cors_allowed_origins=["*"]
)


@sio.event
async def connect(sid, environ, auth):
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

        await sio.save_session(sid, {"user_id": user_id})
        await sio.enter_room(sid, f"user:{user_id}")

        logger.info(f"User {user_id} connected: {sid}")
        return True


@sio.event
async def disconnect(sid):
    session = await sio.get_session(sid)
    logger.info(f"Disconnected: {sid}. Session: {session}")


app = web.Application()

sio.attach(app)

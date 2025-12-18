import logging

import socketio

from aiohttp import web

from configs import config

from ws.default_namespace import DefaultNamespace
from ws.chat_namespace import ChatNamespace

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

sio = socketio.AsyncServer(
    async_mode='aiohttp',
    client_manager=socketio.AsyncRedisManager(config.redis.url),
    cors_allowed_origins=["*"],
    # logger=True,
    # engineio_logger=True,
)

sio.register_namespace(DefaultNamespace('/'))
sio.register_namespace(ChatNamespace('/chat'))

app = web.Application()

sio.attach(app)
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
        logger.info("[Default namespace]: === CONNECT START ===")
        logger.info(f"[Default namespace]: SID: {sid}")
        logger.info(f"[Default namespace]: AUTH RAW: {auth}")
        logger.info(f"[Default namespace]: ORIGIN: {environ.get('HTTP_ORIGIN')}")
        logger.info(f"[Default namespace]: USER-AGENT: {environ.get('HTTP_USER_AGENT')}")

        try:
            async with container(scope=Scope.REQUEST) as nested_container:
                logger.info("[Default namespace]: DI container acquired")

                decoder = await nested_container.get(JwtDecoder)
                logger.info("[Default namespace]: JwtDecoder resolved")

                if not auth:
                    logger.warning("[Default namespace]: Auth is None")
                    return False

                token = auth.get("token")
                if not token:
                    logger.warning("[Default namespace]: Token missing in auth payload")
                    return False

                logger.info(f"[Default namespace]: Token received (len={len(token)})")

                try:
                    payload = decoder.decode(token)
                    logger.info(f"[Default namespace]: JWT decoded successfully: {payload}")
                except Exception as e:
                    logger.exception(f"[Default namespace]: JWT decode failed: {e}")
                    return False

                user_id = payload.get("user_id")
                if not user_id:
                    logger.warning("[Default namespace]: user_id missing in JWT payload")
                    return False

                logger.info(f"[Default namespace]: user_id extracted: {user_id}")

                await self.save_session(sid, {"user_id": user_id})
                logger.info("[Default namespace]: Session saved")

                await self.enter_room(sid, f"user:{user_id}")
                logger.info(f"[Default namespace]: Entered room user:{user_id}")

                logger.info(f"[Default namespace]: User {user_id} connected: {sid}")
                logger.info("[Default namespace]: === CONNECT SUCCESS ===")
                return True

        except Exception as e:
            logger.exception(f"[Default namespace]: UNHANDLED CONNECT ERROR: {e}")
            return False

    async def on_disconnect(self, sid, reason):
        session = await self.get_session(sid)
        logger.info(f"[Default namespace]: Disconnected: {sid}. Session: {session}")
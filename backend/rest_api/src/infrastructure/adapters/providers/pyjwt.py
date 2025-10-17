from datetime import timedelta, datetime, timezone
from typing import Any, Mapping

import jwt

from src.configs import SecurityConfig

from src.application.ports.providers.jwt import JwtProvider

from src.infrastructure.exceptions.auth import InvalidAccessTokenError

class PyJwtProvider(JwtProvider):
    def __init__(self, config: SecurityConfig):
        self._public_key = config.public_key_path.read_text()
        self._private_key = config.private_key_path.read_text()
        self._algorithm = config.algorithm

    def encode(self, payload: Mapping[str, Any], expires_delta: timedelta | None = None) -> str:
        to_encode = dict(payload)

        if expires_delta is not None:
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode["exp"] = expire

        return jwt.encode(to_encode, self._private_key, algorithm=self._algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self._public_key, algorithms=[self._algorithm])
        except jwt.InvalidTokenError:
            raise InvalidAccessTokenError()

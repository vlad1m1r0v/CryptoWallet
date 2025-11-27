from abc import ABC, abstractmethod
from typing import Any

import jwt

from configs import JwtConfig


class JwtDecoder(ABC):
    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]:
        ...


class PyJwtDecoder(JwtDecoder):
    def __init__(self, config: JwtConfig):
        self._public_key = config.public_key_path.read_text()
        self._private_key = config.private_key_path.read_text()
        self._algorithm = config.algorithm

    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self._public_key, algorithms=[self._algorithm])

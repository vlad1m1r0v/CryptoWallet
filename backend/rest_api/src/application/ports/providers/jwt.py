from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Mapping


class JwtProvider(ABC):
    """Interface for generating and verifying JWT tokens."""

    @abstractmethod
    def encode(
        self,
        payload: Mapping[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Generate a JWT token from a payload.
        :param payload: dictionary of claims
        :param expires_delta: optional expiration time
        :return: encoded JWT token string
        """
        ...

    @abstractmethod
    def decode(self, token: str) -> dict[str, Any]:
        """
        Decode a JWT token.
        Raises an exception if the token is invalid or expired.
        :param token: JWT token string
        :return: payload dictionary
        """
        ...
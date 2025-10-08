from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from src.infrastructure.exceptions.auth import AccessTokenNotProvidedError


async def custom_bearer(request: Request) -> str:
    authorization: str = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer" or not credentials:
        raise AccessTokenNotProvidedError()

    return credentials
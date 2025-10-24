from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infrastructure.exceptions.auth import AccessTokenNotProvidedException

bearer_scheme = HTTPBearer(auto_error=False)

async def custom_bearer(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise AccessTokenNotProvidedException()
    return credentials.credentials
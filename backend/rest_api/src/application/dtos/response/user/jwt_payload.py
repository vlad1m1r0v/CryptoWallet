from typing import TypedDict
from uuid import UUID


class JwtPayloadDTO(TypedDict):
    user_id: UUID
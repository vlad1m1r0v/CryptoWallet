from typing import TypedDict, Optional
from uuid import UUID


class GetCurrentUserResponseDTO(TypedDict):
    id: UUID
    username: str
    email: str
    avatar_filename: Optional[str]
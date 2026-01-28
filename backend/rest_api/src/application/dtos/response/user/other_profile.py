from typing import TypedDict, Optional
from uuid import UUID


class OtherProfileResponseDTO(TypedDict):
    id: UUID
    username: str
    avatar_filename: Optional[str]
    total_messages: int
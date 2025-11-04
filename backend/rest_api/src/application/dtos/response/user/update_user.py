from typing import TypedDict, Optional


class UpdateUserResponseDTO(TypedDict):
    username: str
    email: str
    avatar_filename: Optional[str]

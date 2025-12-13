from dataclasses import dataclass
from typing import Optional, TypedDict
from uuid import UUID

@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserDTO:
    user_id: UUID
    username: str

@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserDTO:
    user_id: UUID
    username: Optional[str] = None
    avatar_filename: Optional[str] = None


class UserDTO(TypedDict):
    id: str
    username: str
    avatar_url: str | None
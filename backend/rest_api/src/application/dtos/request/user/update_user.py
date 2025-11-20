from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserRequestDTO:
    user_id: UUID
    avatar: Optional[bytes] = None
    username: Optional[str] = None
    password: Optional[str] = None
    repeat_password: Optional[str] = None

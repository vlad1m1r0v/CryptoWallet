from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserRequestDTO:
    avatar: Optional[bytes] = None
    username: Optional[str] = None
    password: Optional[str] = None
    repeat_password: Optional[str] = None

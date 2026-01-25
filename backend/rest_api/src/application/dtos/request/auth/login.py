from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginUserRequestDTO:
    email: str
    password: str
    remember_me: Optional[bool] = False

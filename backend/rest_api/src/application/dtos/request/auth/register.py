from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterUserRequestDTO:
    username: str
    email: str
    password: str
    repeat_password: str

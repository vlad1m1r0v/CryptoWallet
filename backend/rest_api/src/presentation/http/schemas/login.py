import re
from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints, field_validator

PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=20)]


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: PasswordStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        PATTERN = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,20}$"
        )
        if not re.fullmatch(PATTERN, value):
            raise ValueError(
                "Password must be 8–20 chars, contain upper, lower, digit, special."
            )
        return value


class LoginUserResponseSchema(BaseModel):
    access_token: str

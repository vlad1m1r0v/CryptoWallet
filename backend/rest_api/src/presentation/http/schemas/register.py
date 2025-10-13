from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints, field_validator, model_validator
import re

UsernameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=32)]
PasswordStr = Annotated[str, StringConstraints(min_length=8, max_length=20)]


class RegisterUserSchema(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr
    repeat_password: PasswordStr

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        PATTERN_START = re.compile(r"^[a-zA-Z0-9]")
        PATTERN_ALLOWED_CHARS = re.compile(r"[a-zA-Z0-9._-]*")
        PATTERN_NO_CONSECUTIVE_SPECIALS = re.compile(r"^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$")
        PATTERN_END = re.compile(r".*[a-zA-Z0-9]$")

        if not re.match(PATTERN_START, value):
            raise ValueError("Username must start with a letter or digit.")
        if not re.fullmatch(PATTERN_ALLOWED_CHARS, value):
            raise ValueError("Username contains invalid characters.")
        if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, value):
            raise ValueError("Username has consecutive special characters.")
        if not re.match(PATTERN_END, value):
            raise ValueError("Username must end with a letter or digit.")
        return value

    @field_validator("password", "repeat_password")
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

    @model_validator(mode="after")
    @classmethod
    def passwords_match(cls, model: "RegisterUserSchema") -> "RegisterUserSchema":
        if model.password != model.repeat_password:
            raise ValueError("Passwords do not match.")
        return model


class RegisterUserResponseSchema(BaseModel):
    access_token: str

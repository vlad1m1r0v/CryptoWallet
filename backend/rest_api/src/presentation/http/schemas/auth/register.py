from pydantic import BaseModel, EmailStr, model_validator

from src.presentation.http.schemas.fields import UsernameStr, PasswordStr


class RegisterUserRequestSchema(BaseModel):
    username: UsernameStr
    email: EmailStr
    password: PasswordStr
    repeat_password: PasswordStr

    @model_validator(mode="after")
    @classmethod
    def passwords_match(cls, model: "RegisterUserRequestSchema") -> "RegisterUserRequestSchema":
        if model.password != model.repeat_password:
            raise ValueError("Passwords do not match.")
        return model


class RegisterUserResponseSchema(BaseModel):
    access_token: str

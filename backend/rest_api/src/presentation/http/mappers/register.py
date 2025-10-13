from src.application.interactors.user.register import RegisterUserRequest, RegisterUserResponse

from src.presentation.http.mappers.base import BaseMapper
from src.presentation.http.schemas.register import RegisterUserSchema, RegisterUserResponseSchema


class RegisterUserMapper(BaseMapper[RegisterUserSchema, RegisterUserRequest, RegisterUserResponse]):
    @staticmethod
    def to_request_dto(schema: RegisterUserSchema) -> RegisterUserRequest:
        return RegisterUserRequest(
            username=schema.username,
            email=str(schema.email),
            password=schema.password,
            repeat_password=schema.repeat_password,
        )

    @staticmethod
    def to_response_schema(dto: RegisterUserResponse) -> RegisterUserResponseSchema:
        return RegisterUserResponseSchema(**dto)

from src.application.interactors.user.login import LoginUserRequest, LoginUserResponse

from src.presentation.http.schemas.login import LoginUserSchema, LoginUserResponseSchema
from src.presentation.http.mappers.base import BaseMapper

class LoginUserMapper(BaseMapper[LoginUserSchema, LoginUserRequest, LoginUserResponse]):
    @staticmethod
    def to_request_dto(schema: LoginUserSchema) -> LoginUserRequest:
        return LoginUserRequest(
            email=str(schema.email),
            password=schema.password,
        )

    @staticmethod
    def to_response_schema(dto: LoginUserResponse) -> LoginUserResponseSchema:
        return LoginUserResponseSchema(**dto)
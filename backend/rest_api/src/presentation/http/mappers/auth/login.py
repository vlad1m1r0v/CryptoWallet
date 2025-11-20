from src.application.dtos.request import LoginUserRequestDTO
from src.application.dtos.response import LoginUserResponseDTO

from src.presentation.http.schemas import (
    LoginUserRequestSchema,
    LoginUserResponseSchema
)


class LoginUserMapper:
    @staticmethod
    def to_request_dto(schema: LoginUserRequestSchema) -> LoginUserRequestDTO:
        return LoginUserRequestDTO(
            email=str(schema.email),
            password=schema.password,
        )

    @staticmethod
    def to_response_schema(dto: LoginUserResponseDTO) -> LoginUserResponseSchema:
        return LoginUserResponseSchema(**dto)

from src.application.dtos.request import RegisterUserRequestDTO
from src.application.dtos.response import RegisterUserResponseDTO

from src.presentation.http.schemas import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema
)


class RegisterUserMapper:
    @staticmethod
    def to_request_dto(schema: RegisterUserRequestSchema) -> RegisterUserRequestDTO:
        return RegisterUserRequestDTO(
            username=schema.username,
            email=str(schema.email),
            password=schema.password,
            repeat_password=schema.repeat_password,
        )

    @staticmethod
    def to_response_schema(dto: RegisterUserResponseDTO) -> RegisterUserResponseSchema:
        return RegisterUserResponseSchema(**dto)

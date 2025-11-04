from src.configs import config

from src.application.dtos.request import UpdateUserRequestDTO
from src.application.dtos.response import UpdateUserResponseDTO

from src.presentation.http.mappers.base import BaseMapper
from src.presentation.http.schemas import(
    UpdateUserRequestSchema,
    UpdateUserResponseSchema
)


class UpdateUserMapper(
    BaseMapper[
        UpdateUserRequestDTO,
        UpdateUserResponseDTO,
        UpdateUserRequestSchema,
        UpdateUserResponseSchema
    ]):
    @staticmethod
    async def to_request_dto(schema: UpdateUserRequestSchema) -> UpdateUserRequestDTO:
        return UpdateUserRequestDTO(
            avatar=await schema.avatar.read() if schema.avatar else None,
            username=schema.username,
            password=schema.password,
            repeat_password=schema.repeat_password,
        )

    @staticmethod
    def to_response_schema(dto: UpdateUserResponseDTO) -> UpdateUserResponseSchema:
        return UpdateUserResponseSchema(
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}" if dto["avatar_filename"] else None,
        )
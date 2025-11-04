from src.configs import config

from src.application.dtos.request import GetCurrentUserRequestDTO
from src.application.dtos.response import GetCurrentUserResponseDTO

from src.presentation.http.schemas import (
    GetCurrentUserRequestSchema,
    GetCurrentUserResponseSchema
)

from src.presentation.http.mappers.base import BaseMapper


class GetCurrentUserMapper(
    BaseMapper[
        GetCurrentUserRequestDTO,
        GetCurrentUserResponseDTO,
        GetCurrentUserRequestSchema,
        GetCurrentUserResponseSchema
    ]):
    @staticmethod
    def to_request_dto(schema: GetCurrentUserRequestSchema) -> GetCurrentUserRequestDTO:
        return GetCurrentUserRequestDTO(
            access_token=schema.access_token
        )

    @staticmethod
    def to_response_schema(dto: GetCurrentUserResponseDTO) -> GetCurrentUserResponseSchema:
        return GetCurrentUserResponseSchema(
            id=dto["id"],
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}" if dto["avatar_filename"] else None
        )

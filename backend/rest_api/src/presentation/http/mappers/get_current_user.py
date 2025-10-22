from src.configs import config

from src.presentation.http.schemas.get_current_user import (
    GetCurrentUserSchema,
    GetCurrentUserResponseSchema
)

from src.application.interactors.user.get_current_user import (
    GetCurrentUserRequest,
    GetCurrentUserResponse
)

from src.presentation.http.mappers.base import BaseMapper


class GetCurrentUserMapper(BaseMapper[GetCurrentUserSchema, GetCurrentUserRequest, GetCurrentUserResponse]):
    @staticmethod
    def to_request_dto(schema: GetCurrentUserSchema) -> GetCurrentUserRequest:
        return GetCurrentUserRequest(
            access_token=schema.access_token
        )

    @staticmethod
    def to_response_schema(dto: GetCurrentUserResponse) -> GetCurrentUserResponseSchema:
        return GetCurrentUserResponseSchema(
            id=dto["id"],
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}"
        )

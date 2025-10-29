from src.configs import config

from src.application.interactors.user.update_user import UpdateUserRequest, UpdateUserResponse

from src.presentation.http.mappers.base import BaseMapper
from src.presentation.http.schemas.update_user import UpdateUserSchema, UpdateUserResponseSchema


class UpdateUserMapper(BaseMapper[UpdateUserSchema, UpdateUserRequest, UpdateUserResponse]):
    @staticmethod
    async def to_request_dto(schema: UpdateUserSchema) -> UpdateUserRequest:
        return UpdateUserRequest(
            avatar=await schema.avatar.read() if schema.avatar else None,
            username=schema.username,
            password=schema.password,
            repeat_password=schema.repeat_password,
        )

    @staticmethod
    def to_response_schema(dto: UpdateUserResponse) -> UpdateUserResponseSchema:
        return UpdateUserResponseSchema(
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}"
        )

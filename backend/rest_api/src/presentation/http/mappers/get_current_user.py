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
        return GetCurrentUserResponseSchema(**dto)

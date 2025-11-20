from src.application.dtos.request import UpdateUserRequestDTO

from src.presentation.http.schemas import UpdateUserRequestSchema


class UpdateUserMapper:
    @staticmethod
    async def to_request_dto(schema: UpdateUserRequestSchema) -> UpdateUserRequestDTO:
        return UpdateUserRequestDTO(
            user_id=schema.user_id,
            avatar=await schema.avatar.read() if schema.avatar else None,
            username=schema.username,
            password=schema.password,
            repeat_password=schema.repeat_password,
        )
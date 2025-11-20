from src.configs import config

from src.application.dtos.response import UserResponseDTO

from src.presentation.http.schemas import (
    GetUserResponseSchema,
    GetUserResponseWalletSchema,
    GetUserResponsePermissionsSchema
)


class GetUserMapper:
    @staticmethod
    def to_response_schema(dto: UserResponseDTO) -> GetUserResponseSchema:
        return GetUserResponseSchema(
            id=dto["id"],
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}" if dto["avatar_filename"] else None,
            permissions=GetUserResponsePermissionsSchema(
                has_chat_access=dto["permissions"]["has_chat_access"]
            ),
            wallets=[GetUserResponseWalletSchema(
                id=wallet["id"],
                address=wallet["address"]
            ) for wallet in dto["wallets"]]
        )

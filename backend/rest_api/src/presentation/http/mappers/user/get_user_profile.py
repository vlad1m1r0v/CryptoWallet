from types import NoneType

from src.configs import config

from src.application.dtos.response import GetUserProfileResponseDTO

from src.presentation.http.schemas import (
    GetUserProfileResponseSchema,
    GetUserProfileResponseWalletSchema
)

from src.presentation.http.mappers.base import BaseMapper


class GetUserProfileMapper(
    BaseMapper[
        NoneType,
        GetUserProfileResponseDTO,
        NoneType,
        GetUserProfileResponseSchema
    ]):
    @staticmethod
    def to_request_dto(schema: None) -> None:
        raise NotImplementedError

    @staticmethod
    def to_response_schema(dto: GetUserProfileResponseDTO) -> GetUserProfileResponseSchema:
        return GetUserProfileResponseSchema(
            id=dto["id"],
            username=dto["username"],
            email=dto["email"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}" if dto["avatar_filename"] else None,
            wallets=[GetUserProfileResponseWalletSchema(
                id=wallet["id"],
                address=wallet["address"]
            ) for wallet in dto["wallets"]]
        )

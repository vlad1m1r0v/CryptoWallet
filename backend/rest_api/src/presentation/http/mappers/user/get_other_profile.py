from src.configs import config

from src.application.dtos.response import OtherProfileResponseDTO

from src.presentation.http.schemas import GetOtherProfileResponseSchema


class GetOtherProfileMapper:
    @staticmethod
    def to_response_schema(dto: OtherProfileResponseDTO) -> GetOtherProfileResponseSchema:
        return GetOtherProfileResponseSchema(
            id=dto["id"],
            username=dto["username"],
            total_messages=dto["total_messages"],
            avatar_url=f"{config.s3.base_file_url}/{dto['avatar_filename']}" if dto["avatar_filename"] else None
        )

from src.application.dtos.response import OtherProfileResponseDTO

from src.infrastructure.persistence.database.models import User as UserM


class OtherProfileMapper:
    @staticmethod
    def to_dto(model: UserM) -> OtherProfileResponseDTO:
        return OtherProfileResponseDTO(
            id=model.id,
            username=model.username,
            avatar_filename=model.avatar_filename,
            total_messages=model.total_messages,
        )

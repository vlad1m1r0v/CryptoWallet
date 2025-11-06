from src.application.dtos.response import (
    GetUserProfileResponseDTO,
    GetUserProfileResponseWalletDTO
)

from src.infrastructure.persistence.database.models import User as UserM


class ProfileMapper:
    @staticmethod
    def to_dto(model: UserM) -> GetUserProfileResponseDTO:
        return GetUserProfileResponseDTO(
            id=model.id,
            username=model.username,
            email=model.email,
            avatar_filename=model.avatar_filename,
            wallets=[
                GetUserProfileResponseWalletDTO(
                    id=wallet.id,
                    address=wallet.address
                ) for wallet in model.wallets
            ]
        )

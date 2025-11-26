from src.application.dtos.response import (
    UserResponseDTO,
    UserResponseWalletDTO,
    UserResponsePermissionsDTO
)
from src.domain.entities import User as UserE

from src.infrastructure.persistence.database.models import User as UserM


class UserMapper:
    @staticmethod
    def to_model(entity: UserE) -> UserM:
        return UserM(
            id=entity.id_.value,
            username=entity.username.value,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            avatar_filename=entity.avatar_filename.value if entity.avatar_filename else None,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dto(model: UserM) -> UserResponseDTO:
        return UserResponseDTO(
            id=model.id,
            is_active=model.is_active,
            password_hash=model.password_hash,
            username=model.username,
            email=model.email,
            avatar_filename=model.avatar_filename,
            total_messages=model.total_messages,
            wallets=[
                UserResponseWalletDTO(
                    id=wallet.id,
                    address=wallet.address
                ) for wallet in model.wallets
            ],
            permissions=UserResponsePermissionsDTO(
                has_chat_access=model.permissions.has_chat_access
            )
        )

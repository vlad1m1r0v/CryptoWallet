from src.domain.entities.permissions import Permissions as PermissionsE

from src.infrastructure.persistence.database.models import Permissions as PermissionsM


class PermissionsMapper:
    @staticmethod
    def to_model(entity: PermissionsE) -> PermissionsM:
        return PermissionsM(
            id=entity.id_.value,
            user_id=entity.user_id.value,
            has_chat_access=entity.has_chat_access.value
        )

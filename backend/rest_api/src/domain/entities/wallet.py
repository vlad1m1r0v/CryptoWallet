from src.domain.entities.base import Entity

from src.domain.value_objects import (
    EntityId,
    Address,
    EncryptedPrivateKey,
    Balance,
    Timestamp
)


class Wallet(Entity[EntityId]):
    def __init__(
            self,
            *,
            id_: EntityId,
            user_id: EntityId,
            asset_id: EntityId,
            address: Address,
            encrypted_private_key: EncryptedPrivateKey,
            balance: Balance,
            created_at: Timestamp,
    ) -> None:
        super().__init__(id_=id_)
        self.user_id = user_id
        self.asset_id = asset_id
        self.address = address
        self.encrypted_private_key = encrypted_private_key
        self.balance = balance
        self.created_at = created_at

from src.domain.entities import Wallet

from src.domain.ports import (
    IdGenerator,
    SecretEncryptor
)

from src.domain.value_objects import (
    EntityId,
    Address,
    RawPrivateKey,
    EncryptedPrivateKey,
    Balance,
    Timestamp
)


class WalletService:
    def __init__(
            self,
            id_generator: IdGenerator,
            secret_encryptor: SecretEncryptor,
    ) -> None:
        self._id_generator = id_generator
        self._secret_encryptor = secret_encryptor

    def create_wallet(
            self,
            user_id: EntityId,
            asset_id: EntityId,
            address: Address,
            raw_private_key: RawPrivateKey,
            balance: Balance,
            created_at: Timestamp,
    ) -> Wallet:
        wallet_id = self._id_generator()
        encrypted_private_key = EncryptedPrivateKey(self._secret_encryptor.encrypt(raw_private_key.value))

        return Wallet(
            id_=wallet_id,
            asset_id=asset_id,
            user_id=user_id,
            address=address,
            encrypted_private_key=encrypted_private_key,
            balance=balance,
            created_at=created_at,
        )

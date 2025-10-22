from src.domain.entities.wallet import Wallet

from src.domain.ports.secret_encryptor import SecretEncryptor
from src.domain.ports.id_generator import IdGenerator

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp

from src.domain.value_objects.wallet.address import Address
from src.domain.value_objects.wallet.balance import Balance
from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey


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
        encrypted_private_key = self._secret_encryptor.encrypt(raw_private_key)

        return Wallet(
            id_=wallet_id,
            asset_id=asset_id,
            user_id=user_id,
            address=address,
            encrypted_private_key=encrypted_private_key,
            balance=balance,
            created_at=created_at,
        )

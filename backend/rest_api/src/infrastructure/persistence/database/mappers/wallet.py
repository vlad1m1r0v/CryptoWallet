from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp

from src.domain.value_objects.wallet.address import Address
from src.domain.value_objects.wallet.encrpyted_private_key import EncryptedPrivateKey
from src.domain.value_objects.wallet.balance import Balance

from src.domain.entities.wallet import Wallet as WalletE

from src.infrastructure.persistence.database.models.wallet import Wallet as WalletM
from src.infrastructure.persistence.database.mappers.base import BaseMapper

class WalletMapper(BaseMapper[WalletE, WalletM]):
    @staticmethod
    def to_entity(model: WalletM) -> WalletE:
        return WalletE(
            id_=EntityId(model.id),
            user_id=EntityId(model.user_id),
            asset_id=EntityId(model.asset_id),
            encrypted_private_key=EncryptedPrivateKey(model.private_key),
            address=Address(model.address),
            balance=Balance(model.balance),
            created_at=Timestamp(model.created_at)

        )

    @staticmethod
    def to_model(wallet: WalletE) -> WalletM:
        return WalletM(
            id=wallet.id_.value,
            user_id=wallet.user_id.value,
            asset_id=wallet.asset_id.value,
            private_key=wallet.encrypted_private_key.value,
            address=wallet.address.value,
            balance=wallet.balance.value,
            created_at=wallet.created_at.value,
        )
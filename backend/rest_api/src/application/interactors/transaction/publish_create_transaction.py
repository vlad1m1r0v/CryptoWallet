from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.enums.asset import AssetNetworkTypeEnum

from src.domain.exceptions.wallet import (
    UserIsNotOwnerOfWalletException,
    NotEnoughBalanceOnWalletException
)

from src.domain.ports.secret_encryptor import SecretEncryptor

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.wallet.address import Address
from src.domain.value_objects.wallet.balance import Balance
from src.domain.value_objects.wallet.encrpyted_private_key import EncryptedPrivateKey
from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey

from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.asset import AssetGateway
from src.application.ports.events.event_publisher import EventPublisher


@dataclass(frozen=True, slots=True, kw_only=True)
class PublishCreateTransactionRequest:
    from_address: str
    to_address: str
    amount: Decimal


class PublishCreateTransactionInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            asset_gateway: AssetGateway,
            event_publisher: EventPublisher,
            secret_encryptor: SecretEncryptor
    ) -> None:
        self._asset_gateway = asset_gateway
        self._wallet_gateway = wallet_gateway
        self._event_publisher = event_publisher
        self._secret_encryptor = secret_encryptor

    async def __call__(self, user_id: UUID, data: PublishCreateTransactionRequest) -> None:
        address = Address(data.from_address)
        user_id = EntityId(user_id)
        amount = Balance(data.amount)

        wallet = await self._wallet_gateway.read_by_address(address)

        if wallet.user_id != user_id:
            raise UserIsNotOwnerOfWalletException(user_id, address)

        if wallet.balance < amount:
            raise NotEnoughBalanceOnWalletException()

        encrypted_key: EncryptedPrivateKey = wallet.encrypted_private_key
        decrypted_private_key: RawPrivateKey = self._secret_encryptor.decrypt(encrypted_key)

        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        amount = Decimal(data.amount * (10 ** sepolia_asset.decimals.value))

        return await self._event_publisher.create_transaction(
            private_key=decrypted_private_key.value,
            to_address=data.to_address,
            amount=amount,
        )

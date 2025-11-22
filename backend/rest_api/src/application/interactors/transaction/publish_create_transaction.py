from decimal import Decimal
from uuid import UUID
import logging

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException,
    NotEnoughBalanceOnWalletException
)
from src.domain.ports import SecretEncryptor
from src.domain.value_objects import (
    EntityId,
    Address,
    Balance
)

from src.application.ports.gateways import (
    WalletGateway,
    AssetGateway
)
from src.application.ports.events import EventPublisher
from src.application.dtos.request import PublishCreateTransactionRequestDTO
from src.application.dtos.events import CreateTransactionEventDTO

logger = logging.getLogger(__name__)


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

    async def __call__(self, user_id: UUID, data: PublishCreateTransactionRequestDTO) -> None:
        address = Address(data.from_address)
        user_id = EntityId(user_id)
        amount = Balance(data.amount)

        logger.info("Checking if wallet with given id exists...")

        wallet = await self._wallet_gateway.read(address=address.value)

        if not wallet:
            raise WalletNotFoundException()

        logger.info("Checking if user is owner of wallet...")

        if wallet["user_id"] != user_id.value:
            raise UserIsNotOwnerOfWalletException(user_id, address)

        logger.info("Checking if wallet has enough money for transaction...")

        if wallet["balance"] < amount.value:
            raise NotEnoughBalanceOnWalletException()

        logger.info("Decrypting wallet private key...")

        private_key = self._secret_encryptor.decrypt(wallet["encrypted_private_key"])

        logger.info("Getting Sepolia asset record from database...")

        sepolia_asset = await self._asset_gateway.read(network_type=AssetNetworkTypeEnum.SEPOLIA)

        amount = Decimal(data.amount * (10 ** sepolia_asset["decimals"]))

        logger.info("Emitting event rest_api.create_transaction...")

        return await self._event_publisher.create_transaction(
            CreateTransactionEventDTO(
                private_key=private_key,
                to_address=data.to_address,
                amount=amount
            )
        )

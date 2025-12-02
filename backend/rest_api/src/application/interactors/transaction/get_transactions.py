import logging

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    Address
)

from src.application.ports.gateways import (
    WalletGateway,
    TransactionGateway
)
from src.application.dtos.request import (
    GetTransactionsRequestDTO
)
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionResponseDTO
)

logger = logging.getLogger(__name__)


class GetTransactionsInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway

    async def __call__(self, data: GetTransactionsRequestDTO) -> PaginatedResponseDTO[TransactionResponseDTO]:
        wallet_id = EntityId(data.wallet_id)
        user_id = EntityId(data.user_id)

        wallet = await self._wallet_gateway.read(wallet_id=wallet_id.value)

        logging.info("Checking if wallet with given id exists...")

        if not wallet:
            raise WalletNotFoundException()

        logging.info("Checking if user is owner of wallet...")

        if wallet["user_id"] != user_id.value:
            raise UserIsNotOwnerOfWalletException(user_id=user_id, address=Address(wallet["address"]))

        logging.info("Getting list of transactions from database for wallet...")

        return await self._transaction_gateway.list(
            wallet_id=data.wallet_id,
            sort=data.sort,
            order=data.order,
            page=data.page,
            per_page=data.per_page
        )

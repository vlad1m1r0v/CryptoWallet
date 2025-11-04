from uuid import UUID

from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import EntityId

from src.application.ports.gateways import (
    WalletGateway,
    TransactionGateway
)
from src.application.dtos.request import (
    GetTransactionsRequestDTO
)
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionsListItemResponseDTO
)


class GetTransactionsInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway

    async def __call__(self, user_id: UUID, data: GetTransactionsRequestDTO) -> PaginatedResponseDTO[TransactionsListItemResponseDTO]:
        wallet_id = EntityId(data.wallet_id)
        user_id = EntityId(user_id)

        walletE = await self._wallet_gateway.read_by_id(wallet_id)

        if not walletE:
            raise WalletNotFoundException()

        if walletE.user_id != user_id:
            raise UserIsNotOwnerOfWalletException(user_id=user_id, address=walletE.address)

        return await self._transaction_gateway.get_transactions(
            wallet_id=wallet_id,
            sort_by=data.sort_by,
            order=data.order,
            page=data.page
        )

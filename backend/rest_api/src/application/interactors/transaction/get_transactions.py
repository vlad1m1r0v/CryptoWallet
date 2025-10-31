from typing import Optional
from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions.wallet import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)

from src.domain.value_objects.shared.entity_id import EntityId

from src.application.enums.sort_order import SortOrderEnum

from src.application.dtos.response.paginated_response import PaginatedResult
from src.application.dtos.response.transactions_list import TransactionListItemDTO

from src.application.ports.gateways.wallet import WalletGateway
from src.application.ports.gateways.transaction import (
    SortFieldEnum,
    TransactionGateway
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetTransactionsRequest:
    page: Optional[int] = 1
    wallet_id: UUID
    sort_by: SortFieldEnum
    order: SortOrderEnum


class GetTransactionsInteractor:
    def __init__(
            self,
            wallet_gateway: WalletGateway,
            transaction_gateway: TransactionGateway,
    ) -> None:
        self._wallet_gateway = wallet_gateway
        self._transaction_gateway = transaction_gateway

    async def __call__(self, user_id: UUID, data: GetTransactionsRequest) -> PaginatedResult[TransactionListItemDTO]:
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

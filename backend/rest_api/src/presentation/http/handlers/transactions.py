from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions.wallet import (
    WalletAlreadyExistsException,
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException
)

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)

from src.application.enums.sort_order import SortOrderEnum
from src.application.ports.gateways.transaction import SortFieldEnum

from src.application.interactors.transaction.publish_create_transaction import PublishCreateTransactionInteractor
from src.application.interactors.transaction.get_transactions import GetTransactionsInteractor

from src.presentation.http.schemas.publish_create_transaction import PublishCreateTransactionSchema
from src.presentation.http.mappers.publish_create_transaction import PublishCreateTransactionMapper

from src.presentation.http.schemas.paginated_result import PaginatedResultSchema
from src.presentation.http.schemas.get_transactions import (
    GetTransactionsSchema,
    TransactionListItemSchema
)
from src.presentation.http.mappers.get_transactions import GetTransactionsMapper

from src.presentation.http.dependencies.get_current_user import get_current_user

from src.presentation.http.openapi.examples_generator import generate_examples

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(
        UserIsNotOwnerOfWalletException,
        WalletAlreadyExistsException,
        is_auth=True
    ),
)
@inject
async def create_transaction(
        interactor: FromDishka[PublishCreateTransactionInteractor],
        user: GetCurrentUserResponse = Depends(get_current_user),
        data: PublishCreateTransactionSchema = Body(),
) -> None:
    dto = PublishCreateTransactionMapper.to_request_dto(data)
    return await interactor(user_id=user["id"], data=dto)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        UserIsNotOwnerOfWalletException,
        WalletNotFoundException,
        is_auth=True
    ),
    response_model=PaginatedResultSchema[TransactionListItemSchema],
)
@inject
async def get_transactions(
        interactor: FromDishka[GetTransactionsInteractor],
        user: GetCurrentUserResponse = Depends(get_current_user),
        wallet_id: UUID = Query(),
        sort_by: SortFieldEnum = Query(),
        order: SortOrderEnum = Query(),
        page: int = Query(default=1),
) -> PaginatedResultSchema[TransactionListItemSchema]:
    schema = GetTransactionsSchema(
        page=page,
        wallet_id=wallet_id,
        sort_by=sort_by,
        order=order
    )
    request_dto = GetTransactionsMapper.to_request_dto(schema)
    result = await interactor(user_id=user["id"], data=request_dto)
    return GetTransactionsMapper.to_response_schema(result)

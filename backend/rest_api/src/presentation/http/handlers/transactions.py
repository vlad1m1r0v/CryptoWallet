from uuid import UUID

from fastapi import APIRouter, Depends, Body, Query
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import (
    WalletAlreadyExistsException,
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException
)

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.enums import (
    SortOrderEnum,
    TransactionSortFieldEnum
)
from src.application.interactors import (
    PublishCreateTransactionInteractor,
    GetTransactionsInteractor
)

from src.presentation.http.schemas import (
    PublishCreateTransactionRequestSchema,
    GetTransactionsRequestSchema,
    PaginatedResponseSchema,
    GetTransactionsListItemResponseSchema
)
from src.presentation.http.mappers import (
    PublishCreateTransactionMapper,
    GetTransactionsMapper
)

from src.presentation.http.dependencies import get_current_user

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(
        UserIsNotOwnerOfWalletException,
        WalletAlreadyExistsException,
        WalletNotFoundException,
        is_auth=True
    ),
)
@inject
async def create_transaction(
        interactor: FromDishka[PublishCreateTransactionInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
        data: PublishCreateTransactionRequestSchema = Body(),
) -> None:
    dto = PublishCreateTransactionMapper.to_request_dto(data)
    return await interactor(
        user_id=user["id"],
        data=dto
    )


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        UserIsNotOwnerOfWalletException,
        WalletNotFoundException,
        is_auth=True
    ),
    response_model=PaginatedResponseSchema[GetTransactionsListItemResponseSchema],
)
@inject
async def get_transactions(
        interactor: FromDishka[GetTransactionsInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
        wallet_id: UUID = Query(),
        sort_by: TransactionSortFieldEnum = Query(),
        order: SortOrderEnum = Query(),
        page: int = Query(default=1),
) -> PaginatedResponseSchema[GetTransactionsListItemResponseSchema]:
    schema = GetTransactionsRequestSchema(
        page=page,
        wallet_id=wallet_id,
        sort_by=sort_by,
        order=order
    )
    dto = GetTransactionsMapper.to_request_dto(schema)
    result = await interactor(
        user_id=user["id"],
        data=dto
    )
    return GetTransactionsMapper.to_response_schema(result)

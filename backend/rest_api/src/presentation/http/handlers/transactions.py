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

from src.application.dtos.request import TransactionSortField
from src.application.dtos.response import JwtPayloadDTO
from src.application.enums import SortOrderEnum
from src.application.interactors import (
    PublishCreateTransactionInteractor,
    GetTransactionsInteractor
)

from src.presentation.http.schemas import (
    PublishCreateTransactionRequestSchema,
    GetTransactionsRequestSchema,
    PaginatedResponseSchema,
    TransactionResponseSchema
)
from src.presentation.http.mappers import (
    PublishCreateTransactionMapper,
    GetTransactionsMapper
)

from src.presentation.http.dependencies import jwt_payload

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
        user: JwtPayloadDTO = Depends(jwt_payload),
        data: PublishCreateTransactionRequestSchema = Body(),
) -> None:
    dto = PublishCreateTransactionMapper.to_request_dto(data)
    return await interactor(
        user_id=user["user_id"],
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
    response_model=PaginatedResponseSchema[TransactionResponseSchema],
)
@inject
async def get_transactions(
        interactor: FromDishka[GetTransactionsInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload),
        wallet_id: UUID = Query(),
        sort: TransactionSortField = Query(),
        order: SortOrderEnum = Query(),
        page: int = Query(default=1),
) -> PaginatedResponseSchema[TransactionResponseSchema]:
    schema = GetTransactionsRequestSchema(
        page=page,
        user_id=user["user_id"],
        wallet_id=wallet_id,
        sort=sort,
        order=order
    )
    dto = GetTransactionsMapper.to_request_dto(schema)

    result = await interactor(data=dto)

    return GetTransactionsMapper.to_response_schema(result)

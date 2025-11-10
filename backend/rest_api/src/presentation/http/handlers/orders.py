from fastapi import APIRouter, Depends, Body
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import (
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException,
    ProductNotFoundException
)

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import (
    CreateOrderInteractor
)

from src.presentation.http.schemas import (
    CreateOrderRequestSchema,
    OrderResponseSchema
)
from src.presentation.http.mappers import OrderMapper
from src.presentation.http.dependencies import get_current_user

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        WalletNotFoundException,
        UserIsNotOwnerOfWalletException,
        ProductNotFoundException,
        is_auth=True
    ),
    response_model=OrderResponseSchema
)
@inject
async def create_order(
        interactor: FromDishka[CreateOrderInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
        schema: CreateOrderRequestSchema = Body()
) -> OrderResponseSchema:
    request_dto = await OrderMapper.to_request_dto(schema)

    dto = await interactor(
        user_id=user["id"],
        data=request_dto
    )

    return OrderMapper.to_response_schema(dto)

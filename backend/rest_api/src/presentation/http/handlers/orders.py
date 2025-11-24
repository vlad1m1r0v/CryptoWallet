from fastapi import APIRouter, Depends, Body
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import (
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException,
    ProductNotFoundException
)

from src.application.dtos.response import JwtPayloadDTO
from src.application.interactors import (
    CreateOrderInteractor,
    GetOrdersInteractor
)

from src.presentation.http.schemas import (
    CreateOrderRequestSchema,
    OrderResponseSchema
)
from src.presentation.http.mappers import OrderMapper
from src.presentation.http.dependencies import jwt_payload

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
        user: JwtPayloadDTO = Depends(jwt_payload),
        schema: CreateOrderRequestSchema = Body()
) -> OrderResponseSchema:
    request_dto = await OrderMapper.to_request_dto(schema)

    dto = await interactor(
        user_id=user["user_id"],
        data=request_dto
    )

    return OrderMapper.to_response_schema(dto)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model=list[OrderResponseSchema]
)
@inject
async def get_orders(
        interactor: FromDishka[GetOrdersInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload),
) -> list[OrderResponseSchema]:
    dtos = await interactor(user_id=user["user_id"])
    return OrderMapper.to_response_schema(dtos)

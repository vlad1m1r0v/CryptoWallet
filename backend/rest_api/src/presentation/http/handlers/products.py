from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import (
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException
)

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import (
    CreateProductInteractor,
    GetProductsInteractor
)

from src.presentation.http.schemas import (
    CreateProductRequestSchema,
    ProductResponseSchema
)
from src.presentation.http.mappers import ProductMapper
from src.presentation.http.dependencies import get_current_user

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        WalletNotFoundException,
        UserIsNotOwnerOfWalletException,
        is_auth=True
    ),
    response_model=ProductResponseSchema
)
@inject
async def create_product(
        interactor: FromDishka[CreateProductInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
        wallet_id: UUID = Form(),
        name: str = Form(),
        price: Decimal = Form(),
        photo: UploadFile = File(),
) -> ProductResponseSchema:
    request_schema = CreateProductRequestSchema(
        wallet_id=wallet_id,
        name=name,
        price=price,
        photo=photo,
    )

    request_dto = await ProductMapper.to_request_dto(request_schema)

    dto = await interactor(
        user_id=user["id"],
        data=request_dto
    )

    return ProductMapper.to_response_schema(dto)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model=list[ProductResponseSchema]
)
@inject
async def get_products(
        interactor: FromDishka[GetProductsInteractor],
        _: GetCurrentUserResponseDTO = Depends(get_current_user),
) -> list[ProductResponseSchema]:
    dto = await interactor()
    return ProductMapper.to_response_schema_m2m(dto)

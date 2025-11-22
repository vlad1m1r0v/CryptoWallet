from fastapi import APIRouter, Depends, Body, Request
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import (
    WalletNotFoundException,
    UserIsNotOwnerOfWalletException
)

from src.application.dtos.response import JwtPayloadDTO
from src.application.interactors import (
    PublishCreateWalletInteractor,
    PublishImportWalletInteractor,
    PublishRequestFreeETHInteractor,
    GetWalletsInteractor
)

from src.presentation.http.schemas import (
    ImportWalletRequestSchema,
    FreeETHRequestSchema,
    WalletResponseSchema
)
from src.presentation.http.mappers import WalletMapper
from src.presentation.http.dependencies import jwt_payload
from src.presentation.http.limiter import limiter
from src.presentation.http.exceptions.exceptions import (
    TooManyRequestsException
)
from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(is_auth=True),
)
@inject
async def create_eth_wallet(
        interactor: FromDishka[PublishCreateWalletInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload)
) -> None:
    return await interactor(user_id=user["user_id"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model=list[WalletResponseSchema]
)
@inject
async def get_eth_wallets(
        interactor: FromDishka[GetWalletsInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload)
) -> list[WalletResponseSchema]:
    result = await interactor(user_id=user["user_id"])
    return WalletMapper.to_response_schema(result)


@router.post(
    path="/import",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(is_auth=True),
)
@inject
async def import_eth_wallet(
        interactor: FromDishka[PublishImportWalletInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload),
        data: ImportWalletRequestSchema = Body()
) -> None:
    return await interactor(
        user_id=user["user_id"],
        private_key=data.private_key
    )


@router.post(
    path="/request-free-eth",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(
        TooManyRequestsException,
        WalletNotFoundException,
        UserIsNotOwnerOfWalletException,
        is_auth=True
    ),
)
@limiter.limit("1/hour")
@inject
async def request_free_eth(
        request: Request,
        interactor: FromDishka[PublishRequestFreeETHInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload),
        data: FreeETHRequestSchema = Body()
) -> None:
    return await interactor(
        user_id=user["user_id"],
        wallet_id=data.wallet_id
    )

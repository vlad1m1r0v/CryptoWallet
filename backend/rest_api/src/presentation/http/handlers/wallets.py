from fastapi import APIRouter, Depends, Body
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import (
    PublishCreateWalletInteractor,
    PublishImportWalletInteractor
)

from src.presentation.http.schemas import ImportWalletRequestSchema
from src.presentation.http.dependencies import get_current_user
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
        user: GetCurrentUserResponseDTO = Depends(get_current_user)
) -> None:
    return await interactor(user_id=user["id"])


@router.post(
    path="/import",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(is_auth=True),
)
@inject
async def import_eth_wallet(
        interactor: FromDishka[PublishImportWalletInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
        data: ImportWalletRequestSchema = Body()
) -> None:
    return await interactor(
        user_id=user["id"],
        private_key=data.private_key
    )

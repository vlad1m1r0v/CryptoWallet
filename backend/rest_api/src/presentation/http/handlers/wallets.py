from fastapi import APIRouter, Depends
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)
from src.application.interactors.wallet.publish_create_wallet import PublishCreateWalletInteractor

from src.presentation.http.dependencies.get_current_user import get_current_user

from src.presentation.http.openapi.examples_generator import generate_examples

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(is_auth=True),
)
@inject
async def create_eth_wallet(
        interactor: FromDishka[PublishCreateWalletInteractor],
        user: GetCurrentUserResponse = Depends(get_current_user)
) -> None:
    return await interactor(user_id=user["id"])

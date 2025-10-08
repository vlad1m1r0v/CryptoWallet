from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from src.application.interactors.user.get_current_user import (
    GetCurrentUserRequest,
    GetCurrentUserResponse,
    GetCurrentUserInteractor
)

from src.presentation.http.dependencies.custom_bearer import custom_bearer


@inject
async def get_current_user(
        interactor: FromDishka[GetCurrentUserInteractor],
        access_token: str = Depends(custom_bearer)
) -> GetCurrentUserResponse:
    return await interactor(data=GetCurrentUserRequest(access_token=access_token))

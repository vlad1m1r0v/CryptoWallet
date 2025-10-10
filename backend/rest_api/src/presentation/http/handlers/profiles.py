from dishka import FromDishka
from fastapi import APIRouter, Depends, Body

from dishka.integrations.fastapi import inject

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)
from src.application.interactors.user.update_user import (
    UpdateUserRequest,
    UpdateUserResponse,
    UpdateUserInteractor
)
from src.presentation.http.dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/profiles")


@router.get("/me")
@inject
async def my_profile(
        current_user: GetCurrentUserResponse = Depends(get_current_user),
) -> GetCurrentUserResponse:
    return current_user

@router.patch("/me")
@inject
async def update_my_profile(
        interactor: FromDishka[UpdateUserInteractor],
        current_user: GetCurrentUserResponse = Depends(get_current_user),
        data: UpdateUserRequest = Body()
) -> UpdateUserResponse:
    return await interactor(data=data, user_id=current_user["id"])

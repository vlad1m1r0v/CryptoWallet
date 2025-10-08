from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import inject

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)

from src.presentation.http.dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/profiles")


@router.get("/me")
@inject
async def my_profile(
        current_user: GetCurrentUserResponse = Depends(get_current_user),
) -> GetCurrentUserResponse:
    return current_user

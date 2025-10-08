from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from dishka import FromDishka

from src.application.interactors.user.register import (
    RegisterInteractor,
    RegisterUserRequest,
    RegisterUserResponse
)

from src.application.interactors.user.login import (
    LoginInteractor,
    LoginUserRequest,
    LoginUserResponse
)

router = APIRouter(prefix="/auth")


@router.post("/register")
@inject
async def register(
        request_data: RegisterUserRequest,
        interactor: FromDishka[RegisterInteractor],
) -> RegisterUserResponse:
    return await interactor(request_data)


@router.post("/login")
@inject
async def register(
        request_data: LoginUserRequest,
        interactor: FromDishka[LoginInteractor],
) -> LoginUserResponse:
    return await interactor(request_data)

from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Response
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
        response: Response,
):
    result: RegisterUserResponse = await interactor(request_data)
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,
        samesite="lax"
    )


@router.post("/login")
@inject
async def register(
        request_data: LoginUserRequest,
        interactor: FromDishka[LoginInteractor],
        response: Response,
):
    result: LoginUserResponse = await interactor(request_data)
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,
        samesite="lax"
    )

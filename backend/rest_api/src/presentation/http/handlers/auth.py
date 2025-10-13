from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from dishka import FromDishka

from src.application.interactors.user.register import RegisterInteractor
from src.application.interactors.user.login import LoginInteractor

from src.presentation.http.schemas.register import (
    RegisterUserSchema,
    RegisterUserResponseSchema
)
from src.presentation.http.mappers.register import RegisterUserMapper

from src.presentation.http.schemas.login import (
    LoginUserSchema,
    LoginUserResponseSchema
)
from src.presentation.http.mappers.login import LoginUserMapper

router = APIRouter(prefix="/auth")


@router.post("/register")
@inject
async def register(
        schema: RegisterUserSchema,
        interactor: FromDishka[RegisterInteractor],
) -> RegisterUserResponseSchema:
    dto = RegisterUserMapper.to_request_dto(schema)
    result = await interactor(dto)
    return RegisterUserMapper.to_response_schema(result)


@router.post("/login")
@inject
async def login(
        schema: LoginUserSchema,
        interactor: FromDishka[LoginInteractor],
) -> LoginUserResponseSchema:
    dto = LoginUserMapper.to_request_dto(schema)
    result = await interactor(dto)
    return LoginUserMapper.to_response_schema(result)

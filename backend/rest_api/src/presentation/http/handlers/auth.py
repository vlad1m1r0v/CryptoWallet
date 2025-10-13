from dishka.integrations.fastapi import inject
from dishka import FromDishka

from fastapi import APIRouter
from starlette import status

from src.domain.exceptions.user import (
    EmailAlreadyExistsError,
    EmailNotFoundError,
    PasswordsNotMatchError,
    UserNotActivatedError
)

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

from src.presentation.http.openapi.examples_generator import generate_examples

router = APIRouter(prefix="/auth")


@router.post(
    path="/register",
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(EmailAlreadyExistsError),
    response_model_exclude_none=True,
)
@inject
async def register(
        schema: RegisterUserSchema,
        interactor: FromDishka[RegisterInteractor],
) -> RegisterUserResponseSchema:
    dto = RegisterUserMapper.to_request_dto(schema)
    result = await interactor(dto)
    return RegisterUserMapper.to_response_schema(result)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginUserResponseSchema,
    responses=generate_examples(
        EmailNotFoundError,
        PasswordsNotMatchError,
        UserNotActivatedError
    ),
    response_model_exclude_none=True,
)
@inject
async def login(
        schema: LoginUserSchema,
        interactor: FromDishka[LoginInteractor],
) -> LoginUserResponseSchema:
    dto = LoginUserMapper.to_request_dto(schema)
    result = await interactor(dto)
    return LoginUserMapper.to_response_schema(result)

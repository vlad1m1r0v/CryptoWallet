from dishka.integrations.fastapi import inject
from dishka import FromDishka

from fastapi import APIRouter
from starlette import status

from src.domain.exceptions import (
    EmailAlreadyExistsException,
    EmailNotFoundException,
    WrongPasswordException,
    UserNotActivatedException
)

from src.application.interactors import (
    RegisterInteractor,
    LoginInteractor
)

from src.presentation.http.schemas import (
    RegisterUserRequestSchema,
    RegisterUserResponseSchema,
    LoginUserRequestSchema,
    LoginUserResponseSchema
)
from src.presentation.http.mappers import (
    RegisterUserMapper,
    LoginUserMapper
)

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/register",
    response_model=RegisterUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(EmailAlreadyExistsException),
    response_model_exclude_none=True,
)
@inject
async def register(
        schema: RegisterUserRequestSchema,
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
        EmailNotFoundException,
        WrongPasswordException,
        UserNotActivatedException
    ),
    response_model_exclude_none=True,
)
@inject
async def login(
        schema: LoginUserRequestSchema,
        interactor: FromDishka[LoginInteractor],
) -> LoginUserResponseSchema:
    dto = LoginUserMapper.to_request_dto(schema)
    result = await interactor(dto)
    return LoginUserMapper.to_response_schema(result)

from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)
from src.application.interactors.user.update_user import UpdateUserInteractor

from src.presentation.http.dependencies.get_current_user import get_current_user
from src.presentation.http.mappers.update_user import UpdateUserMapper

from src.presentation.http.schemas.get_current_user import GetCurrentUserResponseSchema
from src.presentation.http.mappers.get_current_user import GetCurrentUserMapper

from src.presentation.http.schemas.update_user import UpdateUserSchema, UpdateUserResponseSchema

from src.presentation.http.openapi.examples_generator import generate_examples

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    path="/me",
    response_model=GetCurrentUserResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def get_my_profile(
        user: GetCurrentUserResponse = Depends(get_current_user),
) -> GetCurrentUserResponseSchema:
    return GetCurrentUserMapper.to_response_schema(user)


@router.patch(
    path="/me",
    response_model=UpdateUserResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def update_my_profile(
        interactor: FromDishka[UpdateUserInteractor],
        avatar: Optional[UploadFile] = File(default=None),
        username: Optional[str] = Form(default=None),
        password: Optional[str] = Form(default=None),
        repeat_password: Optional[str] = Form(default=None),
        current_user: GetCurrentUserResponse = Depends(get_current_user),
) -> UpdateUserResponseSchema:
    schema = UpdateUserSchema(
        avatar=avatar,
        username=username,
        password=password,
        repeat_password=repeat_password
    )

    dto = await UpdateUserMapper.to_request_dto(schema)

    result = await interactor(
        data=dto,
        user_id=current_user["id"]
    )

    return UpdateUserMapper.to_response_schema(result)

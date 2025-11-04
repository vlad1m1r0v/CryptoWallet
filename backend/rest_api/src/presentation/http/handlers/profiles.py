from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import UpdateUserInteractor

from src.presentation.http.dependencies import get_current_user
from src.presentation.http.mappers import (
    UpdateUserMapper,
    GetCurrentUserMapper
)

from src.presentation.http.schemas import (
    GetCurrentUserResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema
)

from src.presentation.http.openapi import generate_examples

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
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
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
        current_user: GetCurrentUserResponseDTO = Depends(get_current_user),
) -> UpdateUserResponseSchema:
    schema = UpdateUserRequestSchema(
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

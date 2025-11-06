from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import UserNotFoundException

from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import (
    GetUserProfileInteractor,
    UpdateUserInteractor
)

from src.presentation.http.dependencies import get_current_user
from src.presentation.http.mappers import (
    UpdateUserMapper,
    GetUserProfileMapper
)

from src.presentation.http.schemas import (
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
    GetUserProfileResponseSchema
)

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    path="/me",
    response_model=GetUserProfileResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def get_my_profile(
        interactor: FromDishka[GetUserProfileInteractor],
        user: GetCurrentUserResponseDTO = Depends(get_current_user),
) -> GetUserProfileResponseSchema:
    dto = await interactor(user["id"])
    return GetUserProfileMapper.to_response_schema(dto)


@router.get(
    path="/{user_id}",
    response_model=GetUserProfileResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(UserNotFoundException, is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def get_user_profile(
        interactor: FromDishka[GetUserProfileInteractor],
        user_id: UUID,
        _: GetCurrentUserResponseDTO = Depends(get_current_user),
) -> GetUserProfileResponseSchema:
    dto = await interactor(user_id)
    return GetUserProfileMapper.to_response_schema(dto)


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
        _: GetCurrentUserResponseDTO = Depends(get_current_user),
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

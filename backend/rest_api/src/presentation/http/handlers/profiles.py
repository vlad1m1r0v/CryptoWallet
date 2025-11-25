from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions import UserNotFoundException

from src.application.dtos.response import JwtPayloadDTO
from src.application.interactors import (
    GetUserInteractor,
    UpdateUserInteractor,
    DeleteAvatarInteractor,
)

from src.presentation.http.dependencies import jwt_payload
from src.presentation.http.mappers import (
    UpdateUserMapper,
    GetUserMapper
)

from src.presentation.http.schemas import (
    UpdateUserRequestSchema,
    GetUserResponseSchema
)

from src.presentation.http.openapi import generate_examples

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    path="/me",
    response_model=GetUserResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def get_my_profile(
        interactor: FromDishka[GetUserInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload),
) -> GetUserResponseSchema:
    dto = await interactor(user["user_id"])
    return GetUserMapper.to_response_schema(dto)


@router.get(
    path="/{user_id}",
    response_model=GetUserResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(UserNotFoundException, is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def get_user_profile(
        interactor: FromDishka[GetUserInteractor],
        user_id: UUID,
        _: JwtPayloadDTO = Depends(jwt_payload),
) -> GetUserResponseSchema:
    dto = await interactor(user_id)
    return GetUserMapper.to_response_schema(dto)


@router.patch(
    path="/me",
    response_model=GetUserResponseSchema,
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
        user: JwtPayloadDTO = Depends(jwt_payload),
) -> GetUserResponseSchema:
    schema = UpdateUserRequestSchema(
        user_id=user["user_id"],
        avatar=avatar,
        username=username,
        password=password,
        repeat_password=repeat_password
    )

    dto = await UpdateUserMapper.to_request_dto(schema)

    result = await interactor(data=dto)

    return GetUserMapper.to_response_schema(result)


@router.delete(
    path="/me/avatar",
    response_model=GetUserResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=generate_examples(is_auth=True),
    response_model_exclude_none=True,
)
@inject
async def delete_my_avatar(
        interactor: FromDishka[DeleteAvatarInteractor],
        user: JwtPayloadDTO = Depends(jwt_payload)
) -> GetUserResponseSchema:
    result = await interactor(user_id=user["user_id"])
    return GetUserMapper.to_response_schema(result)

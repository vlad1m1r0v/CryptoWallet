from dishka import FromDishka
from fastapi import APIRouter, Depends, Body

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
router = APIRouter(prefix="/profiles")


@router.get("/me")
@inject
async def get_my_profile(
        user: GetCurrentUserResponse = Depends(get_current_user),
) -> GetCurrentUserResponseSchema:
    return GetCurrentUserMapper.to_response_schema(user)

@router.patch("/me")
@inject
async def update_my_profile(
        interactor: FromDishka[UpdateUserInteractor],
        current_user: GetCurrentUserResponse = Depends(get_current_user),
        schema: UpdateUserSchema = Body()
) -> UpdateUserResponseSchema:
    dto = UpdateUserMapper.to_request_dto(schema)

    result = await interactor(
        data=dto,
        user_id=current_user["id"]
    )

    return UpdateUserMapper.to_response_schema(result)

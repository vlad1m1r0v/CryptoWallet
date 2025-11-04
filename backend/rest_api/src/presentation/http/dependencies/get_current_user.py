from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from src.application.dtos.request import GetCurrentUserRequestDTO
from src.application.dtos.response import GetCurrentUserResponseDTO
from src.application.interactors import GetCurrentUserInteractor

from src.presentation.http.dependencies.custom_bearer import custom_bearer


@inject
async def get_current_user(
        interactor: FromDishka[GetCurrentUserInteractor],
        access_token: str = Depends(custom_bearer)
) -> GetCurrentUserResponseDTO:
    return await interactor(data=GetCurrentUserRequestDTO(access_token=access_token))

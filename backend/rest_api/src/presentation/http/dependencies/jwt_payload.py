from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends

from src.domain.exceptions import UserNotActivatedException

from src.application.ports.providers import JwtProvider

from src.application.interactors import GetUserInteractor
from src.application.dtos.response import JwtPayloadDTO

from src.presentation.http.dependencies.custom_bearer import custom_bearer


@inject
async def jwt_payload(
        interactor: FromDishka[GetUserInteractor],
        provider: FromDishka[JwtProvider],
        access_token: str = Depends(custom_bearer)
) -> JwtPayloadDTO:
    payload = provider.decode(access_token)

    user = await interactor(user_id=payload["user_id"])

    if not user["is_active"]:
        raise UserNotActivatedException()

    return JwtPayloadDTO(user_id=user["id"])

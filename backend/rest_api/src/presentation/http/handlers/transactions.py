from fastapi import APIRouter, Depends, Body
from starlette import status

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.domain.exceptions.wallet import (
    WalletAlreadyExistsException,
    UserIsNotOwnerOfWalletException
)

from src.application.interactors.user.get_current_user import (
    GetCurrentUserResponse
)

from src.application.interactors.transaction.publish_create_transaction import PublishCreateTransactionInteractor

from src.presentation.http.schemas.publish_create_transaction import PublishCreateTransactionSchema
from src.presentation.http.mappers.publish_create_transaction import PublishCreateTransactionMapper
from src.presentation.http.dependencies.get_current_user import get_current_user
from src.presentation.http.openapi.examples_generator import generate_examples

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_examples(
        UserIsNotOwnerOfWalletException,
        WalletAlreadyExistsException,
        is_auth=True
    ),
)
@inject
async def create_transaction(
        interactor: FromDishka[PublishCreateTransactionInteractor],
        user: GetCurrentUserResponse = Depends(get_current_user),
        data: PublishCreateTransactionSchema = Body(),
) -> None:
    dto = PublishCreateTransactionMapper.to_request_dto(data)
    return await interactor(user_id=user["id"], data=dto)

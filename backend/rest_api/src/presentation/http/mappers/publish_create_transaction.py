from types import NoneType

from src.application.interactors.transaction.publish_create_transaction import PublishCreateTransactionRequest

from src.presentation.http.mappers.base import BaseMapper
from src.presentation.http.schemas.publish_create_transaction import PublishCreateTransactionSchema


class PublishCreateTransactionMapper(
    BaseMapper[PublishCreateTransactionSchema, PublishCreateTransactionRequest, NoneType]):
    @staticmethod
    def to_request_dto(schema: PublishCreateTransactionSchema) -> PublishCreateTransactionRequest:
        return PublishCreateTransactionRequest(
            from_address=schema.from_address,
            to_address=schema.to_address,
            amount=schema.amount
        )

    @staticmethod
    def to_response_schema(dto: NoneType) -> NoneType:
        raise NotImplementedError()

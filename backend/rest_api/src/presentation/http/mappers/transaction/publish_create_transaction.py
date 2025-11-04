from types import NoneType

from src.application.dtos.request import PublishCreateTransactionRequestDTO

from src.presentation.http.mappers.base import BaseMapper
from src.presentation.http.schemas import PublishCreateTransactionRequestSchema


class PublishCreateTransactionMapper(
    BaseMapper[
        PublishCreateTransactionRequestDTO,
        NoneType,
        PublishCreateTransactionRequestSchema,
        NoneType
    ]):
    @staticmethod
    def to_request_dto(schema: PublishCreateTransactionRequestSchema) -> PublishCreateTransactionRequestDTO:
        return PublishCreateTransactionRequestDTO(
            from_address=schema.from_address,
            to_address=schema.to_address,
            amount=schema.amount
        )

    @staticmethod
    def to_response_schema(dto: NoneType) -> NoneType:
        raise NotImplementedError()

from src.application.dtos.request import PublishCreateTransactionRequestDTO
from src.presentation.http.schemas import PublishCreateTransactionRequestSchema


class PublishCreateTransactionMapper:
    @staticmethod
    def to_request_dto(schema: PublishCreateTransactionRequestSchema) -> PublishCreateTransactionRequestDTO:
        return PublishCreateTransactionRequestDTO(
            from_address=schema.from_address,
            to_address=schema.to_address,
            amount=schema.amount
        )
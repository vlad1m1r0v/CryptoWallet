from src.db.models import Order as OrderM
from src.db.dtos import OrderDTO


class OrderMapper:
    @staticmethod
    def to_dto(model: OrderM) -> OrderDTO:
        return OrderDTO(
            id=model.id,
            status=model.status,
            created_at=model.created_at
        )

    @staticmethod
    def to_model(dto: OrderDTO) -> OrderM:
        return OrderM(
            id=dto.id,
            status=dto.status,
            created_at=dto.created_at
        )

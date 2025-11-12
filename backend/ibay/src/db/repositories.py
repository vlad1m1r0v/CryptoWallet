import abc
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.db.dtos import OrderDTO
from src.db.models import Order as OrderM
from src.db.mappers import OrderMapper
from src.enums import OrderStatusEnum


class OrderRepositoryPort(abc.ABC):
    @abc.abstractmethod
    async def get_latest_delivering_order(self) -> OrderDTO | None:
        ...

    @abc.abstractmethod
    async def add_order(self, order: OrderDTO) -> OrderDTO:
        ...

    @abc.abstractmethod
    async def update_order(self, order_id: UUID, status: OrderStatusEnum) -> OrderDTO:
        ...


class OrderRepositoryAdapter(OrderRepositoryPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_order(self, order: OrderDTO) -> OrderDTO:
        model = OrderMapper.to_model(order)
        self._session.add(model)
        await self._session.commit()
        return order

    async def update_order(self, order_id: UUID, status: OrderStatusEnum) -> OrderDTO:
        stmt = (
            update(OrderM)
            .where(OrderM.id == order_id)
            .values(
                status=status,
            )
            .returning(OrderM)
        )

        result = await self._session.execute(stmt)
        await self._session.commit()
        model = result.scalar_one()
        return OrderMapper.to_dto(model)

    async def get_latest_delivering_order(self) -> OrderDTO | None:
        stmt = (
            select(OrderM)
            .where(OrderM.status == OrderStatusEnum.DELIVERING)
            .order_by(OrderM.created_at.desc())
            .limit(1)
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return OrderMapper.to_dto(model)

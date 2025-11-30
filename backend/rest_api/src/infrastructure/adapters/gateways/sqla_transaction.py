from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, func, Select

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Transaction
from src.domain.enums import TransactionStatusEnum

from src.application.enums import SortOrderEnum
from src.application.ports.gateways import TransactionGateway
from src.application.dtos.request import TransactionSortField
from src.application.dtos.response import (
    PaginatedResponseDTO,
    TransactionResponseDTO
)

from src.infrastructure.consts import RECORDS_PER_PAGE
from src.infrastructure.persistence.database.models import (
    Wallet as WalletM,
    Transaction as TransactionM
)
from src.infrastructure.persistence.database.mappers import TransactionMapper


class SqlaTransactionGateway(TransactionGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, transactions: List[Transaction]) -> None:
        models: list[TransactionM] = TransactionMapper.to_model(entities=transactions)
        self._session.add_all(models)

    async def read(self, tx_hash: str) -> list[TransactionResponseDTO]:
        stmt = (
            select(TransactionM)
            .options(joinedload(TransactionM.wallet).joinedload(WalletM.asset))
            .where(TransactionM.transaction_hash == tx_hash)
        )

        result = await self._session.execute(stmt)
        models = result.scalars().all()

        models = sorted(
            models,
            key=lambda m: 1 if m.to_address == m.wallet.address else 0
        )

        return TransactionMapper.to_dto(models=models)

    async def update(
            self,
            created_at: datetime,
            tx_hash: str,
            status: TransactionStatusEnum
    ) -> None:
        stmt = update(TransactionM).where(
            TransactionM.transaction_hash == tx_hash
        ).values(
            created_at=created_at,
            transaction_status=status
        )

        await self._session.execute(stmt)

    async def list(
            self,
            wallet_id: UUID,
            sort: Optional[TransactionSortField] = "created_at",
            order: Optional[SortOrderEnum] = SortOrderEnum.ASC,
            page: Optional[int] = 1
    ) -> PaginatedResponseDTO[TransactionResponseDTO]:
        sort_field_map = {
            "created_at": TransactionM.created_at,
            "transaction_fee": TransactionM.transaction_fee,
            "status": TransactionM.transaction_status
        }
        sort_column = sort_field_map.get(str(sort))

        stmt: Select = (
            select(TransactionM)
            .options(
                joinedload(TransactionM.wallet).joinedload(WalletM.asset)
            )
            .where(TransactionM.wallet_id == wallet_id)
            .order_by(
                sort_column.asc() if order == SortOrderEnum.ASC else sort_column.desc()
            )
        )

        result = await self._session.execute(
            stmt
            .limit(RECORDS_PER_PAGE)
            .offset(RECORDS_PER_PAGE * (page - 1))
        )
        models = result.scalars().unique().all()

        count_stmt = (
            select(func.count())
            .select_from(TransactionM)
            .where(TransactionM.wallet_id == wallet_id)
        )

        total_records = (await self._session.execute(count_stmt)).scalar_one()
        total_pages = (total_records + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

        return TransactionMapper.to_dto(
            models=models,
            page=page,
            total_pages=total_pages
        )

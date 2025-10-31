from typing import Optional

from sqlalchemy import select, update, func

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.transaction import Transaction as TransactionE

from src.domain.value_objects.shared.entity_id import EntityId
from src.domain.value_objects.shared.timestamp import Timestamp
from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus

from src.application.enums.sort_order import SortOrderEnum

from src.application.ports.gateways.transaction import (
    SortFieldEnum,
    TransactionGateway
)

from src.application.dtos.response.paginated_response import PaginatedResult
from src.application.dtos.response.transactions_list import TransactionListItemDTO

from src.infrastructure.consts.pagination import RECORDS_PER_PAGE

from src.infrastructure.persistence.database.models.wallet import Wallet as WalletM
from src.infrastructure.persistence.database.models.transaction import Transaction as TransactionM

from src.infrastructure.persistence.database.mappers.transaction import TransactionMapper
from src.infrastructure.persistence.database.mappers.transactions_list import TransactionsListMapper


class SqlaTransactionGateway(TransactionGateway):
    def __init__(self, session: AsyncSession):
        self._session = session

    def add_many(self, transactions: list[TransactionE]) -> list[TransactionE]:
        models: list[TransactionM] = [TransactionMapper.to_model(e) for e in transactions]
        self._session.add_all(models)
        return transactions

    async def update_many(
            self,
            created_at: Timestamp,
            tx_hash: TransactionHash,
            status: TransactionStatus,
    ) -> list[TransactionE]:
        stmt = update(TransactionM).where(
            TransactionM.transaction_hash == tx_hash.value
        ).values(
            created_at=created_at.value,
            transaction_status=status.value
        ).returning(TransactionM)

        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [TransactionMapper.to_entity(m) for m in models]

    async def get_transactions(
            self,
            wallet_id: EntityId,
            sort_by: Optional[SortFieldEnum] = SortFieldEnum.CREATED_AT,
            order: Optional[SortOrderEnum] = SortOrderEnum.ASC,
            page: Optional[int] = 1
    ) -> PaginatedResult[TransactionListItemDTO]:
        sort_field_map = {
            SortFieldEnum.CREATED_AT: TransactionM.created_at,
            SortFieldEnum.TRANSACTION_FEE: TransactionM.transaction_fee,
            SortFieldEnum.STATUS: TransactionM.transaction_status
        }
        sort_column = sort_field_map.get(sort_by, TransactionM.created_at)

        stmt = (
            select(TransactionM)
            .options(
                joinedload(TransactionM.wallet).joinedload(WalletM.asset)
            )
            .where(TransactionM.wallet_id == wallet_id.value)
            .order_by(
                sort_column.asc() if order == SortOrderEnum.ASC else sort_column.desc()
            )
            .limit(RECORDS_PER_PAGE)
            .offset(RECORDS_PER_PAGE * (page - 1))
        )

        result = await self._session.execute(stmt)
        models = result.scalars().unique().all()

        count_stmt = (
            select(func.count())
            .select_from(TransactionM)
            .where(TransactionM.wallet_id == wallet_id.value)
        )

        total_records = (await self._session.execute(count_stmt)).scalar_one()
        total_pages = (total_records + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

        return TransactionsListMapper.to_paginated_dto(
            models=models,
            page=page,
            total_pages=total_pages,
        )

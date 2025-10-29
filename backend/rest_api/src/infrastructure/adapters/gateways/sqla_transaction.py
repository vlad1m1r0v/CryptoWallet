from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.transaction import Transaction as TransactionE

from src.domain.value_objects.shared.timestamp import Timestamp
from src.domain.value_objects.transaction.hash import TransactionHash
from src.domain.value_objects.transaction.status import TransactionStatus

from src.application.ports.gateways.transaction import TransactionGateway

from src.infrastructure.persistence.database.models.transaction import Transaction as TransactionM
from src.infrastructure.persistence.database.mappers.transaction import TransactionMapper


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

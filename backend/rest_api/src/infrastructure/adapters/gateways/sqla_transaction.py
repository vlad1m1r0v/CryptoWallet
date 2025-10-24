from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.transaction import Transaction as TransactionE

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
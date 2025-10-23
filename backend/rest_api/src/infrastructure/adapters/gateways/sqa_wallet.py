from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.wallet import Wallet as WalletE

from src.application.ports.gateways.wallet import WalletGateway

from src.infrastructure.persistence.database.mappers.wallet import WalletMapper


class SqlaWalletGateway(WalletGateway):

    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, wallet: WalletE) -> WalletE:
        wallet_m = WalletMapper.to_model(wallet)
        self._session.add(wallet_m)

        return wallet
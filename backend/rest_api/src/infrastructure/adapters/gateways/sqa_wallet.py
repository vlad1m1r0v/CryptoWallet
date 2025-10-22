from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.wallet import Wallet as WalletE

from src.application.ports.gateways.wallet import WalletGateway
from src.infrastructure.persistence.database.models.wallet import Wallet


class SqlaWalletGateway(WalletGateway):

    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, wallet: WalletE) -> WalletE:
        self._session.add(
            Wallet(
                id=wallet.id_.value,
                user_id=wallet.user_id.value,
                asset_id=wallet.asset_id.value,
                private_key=wallet.encrypted_private_key.value,
                address=wallet.address.value,
                balance=wallet.balance.value,
                created_at=wallet.created_at.value,
            )
        )
        return wallet
from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Enum, UUID
from sqlalchemy.orm import Mapped, relationship

from src.domain.enums import (
    AssetNetworkTypeEnum,
    AssetTypeEnum,
)

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.wallet import Wallet


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    symbol = Column(String(50), nullable=False, unique=True)

    network = Column(Enum(AssetNetworkTypeEnum, native_enum=False), nullable=False)
    asset_type = Column(Enum(AssetTypeEnum, nativate_enum=False), nullable=True)

    decimals = Column(Integer, nullable=False)
    contract_address = Column(String(100), nullable=True)

    wallets: Mapped[List["Wallet"]] = relationship(
        back_populates="asset",
        uselist=True,
        cascade="all, delete-orphan",
    )

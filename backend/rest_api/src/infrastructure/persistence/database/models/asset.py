from sqlalchemy import Column, Integer, String, Enum, UUID

from src.domain.enums.asset import (
    AssetNetworkTypeEnum,
    AssetTypeEnum,
)

from src.infrastructure.persistence.database.models.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    symbol = Column(String(50), nullable=False, unique=True)

    network = Column(Enum(AssetNetworkTypeEnum), nullable=False)
    asset_type = Column(Enum(AssetTypeEnum), nullable=True)

    decimals = Column(Integer, nullable=False)
    contract_address = Column(String(100), nullable=True)

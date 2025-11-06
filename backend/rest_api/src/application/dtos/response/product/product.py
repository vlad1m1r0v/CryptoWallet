from datetime import datetime
from typing import TypedDict
from decimal import Decimal
from uuid import UUID


class ProductResponseAssetDTO(TypedDict):
    symbol: str
    decimals: int


class ProductResponseWalletDTO(TypedDict):
    asset: ProductResponseAssetDTO


class ProductResponseDTO(TypedDict):
    id: UUID
    name: str
    price: Decimal
    photo_filename: str
    created_at: datetime
    wallet: ProductResponseWalletDTO

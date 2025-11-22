from typing import TypedDict
from decimal import Decimal
from uuid import UUID


class WalletResponseAssetDTO(TypedDict):
    symbol: str
    decimals: int


class WalletResponseDTO(TypedDict):
    id: UUID
    user_id: UUID
    address: str
    balance: Decimal
    encrypted_private_key: bytes
    asset: WalletResponseAssetDTO
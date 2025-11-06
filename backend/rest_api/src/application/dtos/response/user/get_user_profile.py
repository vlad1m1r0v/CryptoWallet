from typing import TypedDict, List, Optional
from uuid import UUID


class GetUserProfileResponseWalletDTO(TypedDict):
    id: UUID
    address: str


class GetUserProfileResponseDTO(TypedDict):
    id: UUID
    username: str
    email: str
    avatar_filename: Optional[str]
    wallets: List[GetUserProfileResponseWalletDTO]

from typing import TypedDict, List, Optional
from uuid import UUID


class UserResponseWalletDTO(TypedDict):
    id: UUID
    address: str


class UserResponsePermissionsDTO(TypedDict):
    has_chat_access: bool


class UserResponseDTO(TypedDict):
    id: UUID
    is_active: bool
    password_hash: bytes
    username: str
    email: str
    avatar_filename: Optional[str]
    permissions: UserResponsePermissionsDTO
    wallets: List[UserResponseWalletDTO]

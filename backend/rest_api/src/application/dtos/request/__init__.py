from src.application.dtos.request.auth import (
    LoginUserRequestDTO,
    RegisterUserRequestDTO
)

from src.application.dtos.request.user import (
    GetCurrentUserRequestDTO,
    UpdateUserRequestDTO
)

from src.application.dtos.request.wallet import (
    SaveCreateWalletRequestDTO,
    SaveImportWalletRequestTransactionDTO,
    SaveImportWalletRequestDTO
)

from src.application.dtos.request.transaction import (
    PublishCreateTransactionRequestDTO,
    CreatePendingTransactionRequestDTO,
    UpdateTransactionRequestDTO,
    GetTransactionsRequestDTO
)

from src.application.dtos.request.product import (
    CreateProductRequestDTO
)

__all__ = [
    "LoginUserRequestDTO",
    "RegisterUserRequestDTO",
    "UpdateUserRequestDTO",
    "GetCurrentUserRequestDTO",
    "SaveCreateWalletRequestDTO",
    "SaveImportWalletRequestTransactionDTO",
    "SaveImportWalletRequestDTO",
    "PublishCreateTransactionRequestDTO",
    "CreatePendingTransactionRequestDTO",
    "UpdateTransactionRequestDTO",
    "GetTransactionsRequestDTO",
    "CreateProductRequestDTO",
]

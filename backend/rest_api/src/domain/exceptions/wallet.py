from string import Template

from src.domain.exceptions.base import DomainException

from src.domain.value_objects import (
    EntityId,
    Address
)


class WalletAlreadyExistsException(DomainException):
    message = Template("Wallet with address '$address' has been already imported.")
    example_args = {"address": "0xf04555b42b45E5283F28737D6BA65AE16878D84B"}

    def __init__(self, address: Address):
        super().__init__(address=address.value)


class UserIsNotOwnerOfWalletException(DomainException):
    message = Template("Current user with id '$user_id' is not the owner of wallet with address '$address'.")
    example_args = {
        "user_id": "019a0b8c-c5f1-7666-b8d3-74bb8b55aae2",
        "address": "0xf04555b42b45E5283F28737D6BA65AE16878D84B"
    }

    def __init__(self, user_id: EntityId, address: Address):
        super().__init__(user_id=user_id, address=address.value)


class NotEnoughBalanceOnWalletException(DomainException):
    message = "Not enough balance on wallet."


class WalletNotFoundException(DomainException):
    message = "Wallet was not found."

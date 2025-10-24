from string import Template

from src.domain.exceptions.base import DomainError

from src.domain.value_objects.wallet.address import Address


class WalletAlreadyExistsException(DomainError):
    message = Template("Wallet with address '$address' has been already imported.")
    example_args = {"address": "0xf04555b42b45E5283F28737D6BA65AE16878D84B"}

    def __init__(self, address: Address):
        super().__init__(address=address.value)
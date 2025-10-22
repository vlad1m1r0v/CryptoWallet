from abc import ABC, abstractmethod

from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey
from src.domain.value_objects.wallet.encrpyted_private_key import EncryptedPrivateKey


class SecretEncryptor(ABC):
    @abstractmethod
    def encrypt(self, data: RawPrivateKey) -> EncryptedPrivateKey:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted_key: EncryptedPrivateKey) -> RawPrivateKey:
        raise NotImplementedError

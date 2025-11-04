from abc import ABC, abstractmethod

from src.domain.value_objects import (
    RawPrivateKey,
    EncryptedPrivateKey
)


class SecretEncryptor(ABC):
    @abstractmethod
    def encrypt(self, data: RawPrivateKey) -> EncryptedPrivateKey:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted_key: EncryptedPrivateKey) -> RawPrivateKey:
        raise NotImplementedError

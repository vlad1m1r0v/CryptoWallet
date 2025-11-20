from abc import ABC, abstractmethod


class SecretEncryptor(ABC):
    @abstractmethod
    def encrypt(self, data: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted_key: bytes) -> str:
        raise NotImplementedError

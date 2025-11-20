import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from src.configs import SecurityConfig

from src.domain.ports import SecretEncryptor


class AESSecretEncryptor(SecretEncryptor):
    def __init__(self, security_config: SecurityConfig):
        self._key = security_config.aes_secret_key.encode("utf8")
        self._backend = default_backend()

    def encrypt(self, raw_private_key: str) -> bytes:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv), backend=self._backend)
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(raw_private_key.encode()) + encryptor.finalize()

        return iv + encrypted

    def decrypt(self, encrypted_key: bytes) -> str:
        iv = encrypted_key[:16]
        ciphertext = encrypted_key[16:]
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv), backend=self._backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted.decode()

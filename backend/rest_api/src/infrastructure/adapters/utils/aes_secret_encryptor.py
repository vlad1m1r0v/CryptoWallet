import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from src.configs import SecurityConfig

from src.domain.value_objects.wallet.raw_private_key import RawPrivateKey
from src.domain.value_objects.wallet.encrpyted_private_key import EncryptedPrivateKey

from src.domain.ports.secret_encryptor import SecretEncryptor


class AESSecretEncryptor(SecretEncryptor):
    def __init__(self, security_config: SecurityConfig):
        self._key = security_config.aes_secret_key.encode("utf8")
        self._backend = default_backend()

    def encrypt(self, raw_private_key: RawPrivateKey) -> EncryptedPrivateKey:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv), backend=self._backend)
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(raw_private_key.value.encode()) + encryptor.finalize()

        return EncryptedPrivateKey(iv + encrypted)

    def decrypt(self, encrypted_key: EncryptedPrivateKey) -> RawPrivateKey:
        encrypted_data = encrypted_key.value

        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(self._key), modes.CFB(iv), backend=self._backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        return RawPrivateKey(decrypted.decode())

import bcrypt
import hmac
import hashlib
import base64

from src.configs import SecurityConfig

from src.domain.ports import PasswordHasher

from src.domain.value_objects import (
    PasswordHash,
    RawPassword
)


class BcryptPasswordHasher(PasswordHasher):
    """
    Безпечний PasswordHasher з використанням HMAC + bcrypt.
    - HMAC: для додаткової безпеки (pepper)
    - bcrypt: для стійкого хешування паролів
    """

    def __init__(self, config: SecurityConfig):
        self._pepper = config.password_pepper

    def hash(self, raw_password: RawPassword) -> PasswordHash:
        prehashed = self._prehash(raw_password)
        salt = bcrypt.gensalt()
        return PasswordHash(bcrypt.hashpw(prehashed, salt))

    def verify(self, raw_password: RawPassword, hashed_password: PasswordHash) -> bool:
        prehashed = self._prehash(raw_password)
        return bcrypt.checkpw(prehashed, hashed_password.value)

    def _prehash(self, raw_password: RawPassword) -> bytes:
        """
        HMAC-SHA256 + base64 для стабільної довжини та захисту від null-байтів.
        """
        hmac_digest = hmac.new(
            key=self._pepper.encode(),
            msg=raw_password.value.encode(),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(hmac_digest)
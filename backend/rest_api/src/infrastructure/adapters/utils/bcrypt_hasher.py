import bcrypt
import hmac
import hashlib
import base64

from src.configs import SecurityConfig

from src.domain.ports import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """
    Безпечний PasswordHasher з використанням HMAC + bcrypt.
    - HMAC: для додаткової безпеки (pepper)
    - bcrypt: для стійкого хешування паролів
    """

    def __init__(self, config: SecurityConfig):
        self._pepper = config.password_pepper

    def hash(self, raw_password: str) -> bytes:
        prehashed = self._prehash(raw_password)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(prehashed, salt)

    def verify(self, raw_password: str, hashed_password: bytes) -> bool:
        prehashed = self._prehash(raw_password)
        return bcrypt.checkpw(prehashed, hashed_password)

    def _prehash(self, raw_password: str) -> bytes:
        """
        HMAC-SHA256 + base64 для стабільної довжини та захисту від null-байтів.
        """
        hmac_digest = hmac.new(
            key=self._pepper.encode(),
            msg=raw_password.encode(),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(hmac_digest)
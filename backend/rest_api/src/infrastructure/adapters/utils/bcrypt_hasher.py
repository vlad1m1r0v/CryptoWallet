import base64
import hashlib
import hmac

import bcrypt

from src.configs import SecurityConfig
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.value_objects.raw_password import RawPassword


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, config: SecurityConfig):
        self._pepper = config.password_pepper

    def hash(self, raw_password: RawPassword) -> str:
        prehashed = self._prehash(raw_password)
        return bcrypt.hashpw(prehashed, bcrypt.gensalt()).decode('utf-8')  # зберігаємо str

    def verify(self, *, raw_password: RawPassword, hashed_password: bytes) -> bool:
        prehashed = self._prehash(raw_password)
        return bcrypt.checkpw(prehashed, hashed_password)

    def _prehash(self, raw_password: RawPassword) -> bytes:
        hmac_digest = hmac.new(
            key=self._pepper.encode(),
            msg=raw_password.value.encode(),
            digestmod=hashlib.sha256,
        ).digest()  # raw bytes, не hex
        # base64 дає ASCII байти, які безпечні для bcrypt
        return base64.b64encode(hmac_digest)
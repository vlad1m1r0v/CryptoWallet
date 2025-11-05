from slowapi import Limiter
from slowapi.util import get_remote_address

from src.configs import config

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1/hour"],
    storage_uri=config.redis.url
)

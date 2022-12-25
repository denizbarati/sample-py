from functools import lru_cache
import redis
from pydantic import BaseSettings, RedisDsn, PostgresDsn

_env = None


class Settings(BaseSettings):
    redis_url: RedisDsn
    sqlalchemy_database_url: str
    jwt_pubkey: str
    debug: bool
    port: str
    host: str
    origin: str
    service_name: str
    otel_server: str
    debug: bool
    header_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


def get_redis() -> redis.Redis:
    red_client = redis.Redis(host=settings.redis_url.host, port=settings.redis_url.port, decode_responses=True)
    try:
        yield red_client
    finally:
        red_client.close()

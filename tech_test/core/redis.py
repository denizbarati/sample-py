from tech_test.core.config import get_settings
import aioredis
import asyncio

env = get_settings()

redis = aioredis.from_url(env.redis_url)


async def get_from_redis(key: str):
    value = await redis.get(key)
    print(value)
    return value


async def set_in_redis(value: str, key: str):
    value = await redis.set(key, value)
    return value

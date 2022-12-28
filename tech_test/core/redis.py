import asyncio

import aioredis

redis = aioredis.from_url("redis://localhost/1")

async def get_from_redis(key: str):
    value = await redis.get(key)
    print(value)
    return value


async def set_in_redis(value: str, key: str):
    value = await redis.set(key, value)
    return value


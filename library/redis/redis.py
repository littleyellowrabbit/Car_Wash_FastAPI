from typing import Optional, AsyncGenerator
import redis.asyncio as aioredis
import library.file.config_redis as f_cr

redis_pool : Optional[aioredis.ConnectionPool] = None

def init_redis_session() -> None:
    global redis_pool
    if redis_pool is not None:
        return
    redis_host, redis_port, redis_password = f_cr.read_redis_config()
    redis_pool = aioredis.ConnectionPool(host=redis_host, port=int(redis_port), password=redis_password, db=0,decode_responses=True, retry_on_timeout=True, max_connections=20, socket_timeout=1.0, socket_connect_timeout=1.0)

async def close_redis_session() -> None:
    global redis_pool
    if redis_pool is not None:
        await redis_pool.disconnect()
        redis_pool = None

async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    if redis_pool is None:
        raise RuntimeError("redis_pool is None")
    async with aioredis.Redis(connection_pool=redis_pool) as client:
        yield client

async def set_with_expiry(client: aioredis.Redis, key: str, value: str, expiry_seconds: int =None, ) -> None:
    await client.set(key, value, ex=expiry_seconds)

async def get_value(client: aioredis.Redis, key: str) -> Optional[str]:
    return await client.get(key)

async def exists(client: aioredis.Redis, key: str) -> bool:
    return await client.exists(key) == 1

async def key_delete(client: aioredis.Redis, key:str) -> None:
    if key is None:
        return
    #redis.delete() whether exist or not,always no error.
    await client.delete(key)
    return

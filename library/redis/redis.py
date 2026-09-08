from typing import Optional
import redis.asyncio as aioredis
import library.file.config_redis as f_cr

redis_session : Optional[aioredis.Redis] = None

def init_redis_session() -> None:
    global redis_session
    redis_host, redis_port, redis_password = f_cr.read_redis_config()
    redis_session = aioredis.Redis(host=redis_host, port=int(redis_port), password=redis_password, db=0,decode_responses=True)


async def set_with_expiry(key: str, value: str, expiry_seconds: int =None) -> None:
    await redis_session.set(key, value, ex=expiry_seconds)

async def get_value(key: str) -> Optional[str]:
    return await redis_session.get(key)

async def exists(key: str) -> bool:
    return await redis_session.exists(key) == 1

async def key_delete(key:str) -> None:
    if key is None:
        return
    #redis.delete() whether exist or not,always no error.
    await redis_session.delete(key)
    return

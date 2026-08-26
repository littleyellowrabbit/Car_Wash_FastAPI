from typing import Optional
import redis
import library.file.config_redis as f_cr

redis_session : Optional[redis.Redis] = None

def init_redis_session() -> None:
    global redis_session
    redis_password, redis_host, redis_port = f_cr.read_redis_config()
    redis_session = redis.Redis(host=redis_host, port=int(redis_port), password=redis_password, db=0,decode_responses=True)


def set_with_expiry(key: str, value: str, expiry_seconds: int) -> None:
    redis_session.set(key, value, ex=expiry_seconds)

def get_value(key: str) -> Optional[str]:
    return redis_session.get(key)

def exists(key: str) -> bool:
    return redis_session.exists(key) == 1

def key_delete(key:str) -> None:
    if key is None:
        return
    #redis.delete() whether exist or not,always no error.
    redis_session.delete(key)
    return


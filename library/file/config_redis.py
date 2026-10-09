import configparser
from pathlib import Path
from typing import Optional

_REDIS_CONFIG_CACHE : Optional[tuple[str,str,str]] =None

def read_redis_config() -> tuple[str,str,str]:
    global _REDIS_CONFIG_CACHE
    if _REDIS_CONFIG_CACHE is None:
        base_path = Path(__file__).parent.parent.parent
        config_file = base_path / 'config' / 'redis_config.ini'

        redis_config = configparser.ConfigParser()
        redis_config.read(config_file,encoding='utf-8')

        redis_password = redis_config.get('redis_setting', 'Password')
        redis_host = redis_config.get('redis_setting', 'Host')
        redis_port = redis_config.get('redis_setting', 'Port')

        _REDIS_CONFIG_CACHE = (redis_host, redis_port, redis_password)
    return _REDIS_CONFIG_CACHE


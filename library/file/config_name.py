import configparser
from pathlib import Path
from typing import Optional

redis_name : Optional[dict[str,str]] = None

def get_redis_name() -> dict[str,str]:
    global redis_name
    if redis_name is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        config_path = base_path / 'library' / 'file' / 'name_config.ini'

        config = configparser.ConfigParser()
        config.read(str(config_path), encoding='utf-8')
        token_access_name = config.get('name_setting','token_access')
        token_access_black_name = config.get('name_setting', 'token_access_black')
        token_refresh_name = config.get('name_setting','token_refresh')

        redis_name = {
            'token_access_name':token_access_name,
            'token_access_black_name':token_access_black_name,
            'token_refresh_name':token_refresh_name
        }
    return redis_name


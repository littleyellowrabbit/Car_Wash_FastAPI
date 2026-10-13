import configparser
from pathlib import Path
from typing import Optional

_SQL_CONFIG_CACHE : Optional[tuple[str,str,str,str]] = None

def read_sql_config() -> tuple[str,str,str,str]:
    global _SQL_CONFIG_CACHE
    if _SQL_CONFIG_CACHE is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        sql_config_path = base_path / 'config' / 'sql_config_lofi.ini'

        sql_config = configparser.ConfigParser()
        sql_config.read(str(sql_config_path), encoding='utf-8')

        sql_user = sql_config.get('sql_setting', 'user')
        sql_password = sql_config.get('sql_setting', 'password')
        sql_host = sql_config.get('sql_setting', 'host')
        sql_database = sql_config.get('sql_setting', 'database')

        _SQL_CONFIG_CACHE = (sql_user, sql_password, sql_host, sql_database)
    return _SQL_CONFIG_CACHE

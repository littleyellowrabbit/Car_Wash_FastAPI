import configparser
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent.parent

def read_sql_config() -> tuple[str,str,str,str]:
    sql_config_path = base_path / 'config' / 'sql_config_tEST.ini'
    sql_config = configparser.ConfigParser()
    sql_config.read(str(sql_config_path), encoding='utf-8')
    sql_user = sql_config.get('sql_setting', 'user')
    sql_password = sql_config.get('sql_setting', 'password')
    sql_host = sql_config.get('sql_setting', 'host')
    sql_port = sql_config.get('sql_setting', 'port')
    return sql_user, sql_password, sql_host, sql_port

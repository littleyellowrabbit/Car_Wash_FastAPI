import configparser
from pathlib import Path
from typing import Optional

redis_name : Optional[dict[str,str]] = None

def get_redis_name() -> dict[str,str]:
    global redis_name
    if redis_name is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        config_path = base_path / 'config' / 'name_config.ini'

        config = configparser.ConfigParser()
        config.read(str(config_path), encoding='utf-8')
        # token in decode auto check "exp"
        #token_access_name = config.get('name_setting','token_access')
        token_access_black_name = config.get('name_setting', 'token_access_black')
        token_refresh_name = config.get('name_setting','token_refresh')
        parameter_water_pressure_name = config.get('name_setting', 'parameter_water_pressure')
        parameter_foam_type_name = config.get('name_setting', 'parameter_foam_type')
        parameter_wax_type_name = config.get('name_setting', 'parameter_wax_type')
        parameter_air_pressure_name = config.get('name_setting', 'parameter_air_pressure')
        real_data_name = config.get('name_setting', 'read_data')
        watchdog_name = config.get('name_setting', 'watchdog')


        redis_name = {
            # token in decode auto check "exp"
            #'token_access_name':token_access_name,
            'token_access_black_name':token_access_black_name,
            'token_refresh_name':token_refresh_name,
            'parameter_water_pressure_name':parameter_water_pressure_name,
            'parameter_foam_type_name':parameter_foam_type_name,
            'parameter_wax_type_name': parameter_wax_type_name,
            'parameter_air_pressure_name': parameter_air_pressure_name,
            'real_data_name': real_data_name,
            'watchdog': watchdog_name,
        }
    return redis_name

get_redis_name()


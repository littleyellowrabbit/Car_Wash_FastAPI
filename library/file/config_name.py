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
        parameter_process_start_name = config.get('name_setting', 'parameter_process_start')
        water_pressure_name = config.get('name_setting', 'water_pressure')
        foam_type_name = config.get('name_setting', 'foam_type')
        wax_type_name = config.get('name_setting', 'wax_type')
        air_pressure_name = config.get('name_setting', 'air_pressure')

        water_pressure_used_name = config.get('name_setting', 'water_pressure_used')
        foam_type_used_name = config.get('name_setting', 'foam_type_used')
        wax_type_used_name = config.get('name_setting', 'wax_type_used')
        air_pressure_used_name = config.get('name_setting', 'air_pressure_used')
        standby_status_name = config.get('name_setting', 'standby_status')
        preclean_status_name = config.get('name_setting', 'preclean_status')
        chemical_soft_status_name = config.get('name_setting', 'chemical_soft_status')
        physical_clean_status_name = config.get('name_setting', 'physical_clean_status')
        wax_protect_status_name = config.get('name_setting', 'wax_protect_status')
        dry_air_status_name = config.get('name_setting', 'dry_air_status')
        process_start_name = config.get('name_setting', 'process_start')
        process_start_time_name = config.get('name_setting', 'process_start_time')
        process_end_time_name = config.get('name_setting', 'process_end_time')
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
            'parameter_process_start_name': parameter_process_start_name,
            'water_pressure_name': water_pressure_name,
            'foam_type_name': foam_type_name,
            'wax_type_name': wax_type_name,
            'air_pressure_name': air_pressure_name,
            'water_pressure_used_name': water_pressure_used_name,
            'foam_type_used_name': foam_type_used_name,
            'wax_type_used_name': wax_type_used_name,
            'air_pressure_used_name': air_pressure_used_name,
            'standby_status_name': standby_status_name,
            'preclean_status_name': preclean_status_name,
            'chemical_soft_status_name': chemical_soft_status_name,
            'physical_clean_status_name': physical_clean_status_name,
            'wax_protect_status_name': wax_protect_status_name,
            'dry_air_status_name': dry_air_status_name,
            'process_start_name': process_start_name,
            'process_start_time_name': process_start_time_name,
            'process_end_time_name': process_end_time_name,
            'watchdog_name': watchdog_name,
        }
    return redis_name

get_redis_name()


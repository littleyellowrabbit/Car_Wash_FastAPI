import configparser
from pathlib import Path
from typing import Optional
from library.file.config_name import redis_name

PLC_DEFAULT_CACHE : Optional[dict] =None

def _plc_default() -> dict:
    global PLC_DEFAULT_CACHE
    if PLC_DEFAULT_CACHE is None:
        base_path = Path(__file__).parent.parent.parent
        config_file = base_path / 'config' / 'plc_simulator_default.ini'

        plc_simulator_default = configparser.ConfigParser()
        plc_simulator_default.read(config_file,encoding='utf-8')


        PLC_DEFAULT_CACHE = {redis_name.get('parameter_water_pressure_name'): int(plc_simulator_default.get('default_setting','parameter_water_pressure')),
                              redis_name.get('parameter_foam_type_name'): int(plc_simulator_default.get('default_setting','parameter_foam_type')),
                              redis_name.get('parameter_wax_type_name'): int(plc_simulator_default.get('default_setting','parameter_wax_type')),
                              redis_name.get('parameter_air_pressure_name'): int(plc_simulator_default.get('default_setting','parameter_air_pressure')),
                              redis_name.get('parameter_process_start_name'): int(plc_simulator_default.get('default_setting','parameter_process_start')),
                              redis_name.get('water_pressure_name'): int(plc_simulator_default.get('default_setting','water_pressure')),
                              redis_name.get('foam_type_name'): plc_simulator_default.get('default_setting','foam_type'),
                              redis_name.get('wax_type_name'): plc_simulator_default.get('default_setting','wax_type'),
                              redis_name.get('air_pressure_name'): int(plc_simulator_default.get('default_setting','air_pressure')),
                              redis_name.get('water_pressure_used_name'): int(plc_simulator_default.get('default_setting','water_pressure_used')),
                              redis_name.get('foam_type_used_name'): int(plc_simulator_default.get('default_setting','foam_type_used')),
                              redis_name.get('wax_type_used_name'): int(plc_simulator_default.get('default_setting','wax_type_used')),
                              redis_name.get('air_pressure_used_name'): int(plc_simulator_default.get('default_setting','air_pressure_used')),
                              redis_name.get('standby_status_name'): int(plc_simulator_default.get('default_setting','standby_status')),
                              redis_name.get('preclean_status_name'): int(plc_simulator_default.get('default_setting','preclean_status')),
                              redis_name.get('chemical_soft_status_name'): int(plc_simulator_default.get('default_setting','chemical_soft_status')),
                              redis_name.get('physical_clean_status_name'): int(plc_simulator_default.get('default_setting','physical_clean_status')),
                              redis_name.get('wax_protect_status_name'): int(plc_simulator_default.get('default_setting','wax_protect_status')),
                              redis_name.get('dry_air_status_name'): int(plc_simulator_default.get('default_setting','dry_air_status')),
                              redis_name.get('process_start_name'): int(plc_simulator_default.get('default_setting','process_start')),
                              redis_name.get('process_start_time_name'): float(plc_simulator_default.get('default_setting','process_start_time')),
                              redis_name.get('process_end_time_name'): float(plc_simulator_default.get('default_setting','process_end_time')),
                              redis_name.get('watchdog_name'): float(plc_simulator_default.get('default_setting','watchdog')),
                              }

    return PLC_DEFAULT_CACHE

_plc_default()
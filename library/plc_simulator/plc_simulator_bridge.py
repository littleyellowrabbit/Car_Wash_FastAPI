import redis, json, time, random
import library.file.config_redis as f_cr
from library.file.config_name import redis_name
from typing import Optional
from library.file.config_plc_simulator_default import PLC_DEFAULT_CACHE



running_flag = {"active": True}
parameter_dict: Optional[dict]= {}
redis_host, redis_port, redis_password = f_cr.read_redis_config()
current_data_dict: Optional[dict]= {}

set_pool = redis.ConnectionPool(
    host=redis_host,
    port=int(redis_port),
    password=redis_password,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    retry_on_timeout=True,
    max_connections=20
)

pubsub_pool = redis.ConnectionPool(
    host=redis_host,
    port=int(redis_port),
    password=redis_password,
    db=0,
    decode_responses=True,
    socket_connect_timeout=1,
    retry_on_timeout=True,
    max_connections=5
)

set_client = redis.Redis(connection_pool=set_pool)
pubsub_client = redis.Redis(connection_pool=pubsub_pool)

for key, value in PLC_DEFAULT_CACHE.items():
    if set_client.exists(key) == 1:
        pass
    else:
        set_client.set(key, value)

plc_data_new = PLC_DEFAULT_CACHE.copy()
plc_data_old = PLC_DEFAULT_CACHE.copy()


def plc_client() -> None:
    global parameter_dict
    global current_data_dict
    loop_time = 0.1
    while running_flag["active"]:
        try:
            pubsub_client.ping()
            with pubsub_client.pubsub(ignore_subscribe_messages=True) as pubsub:
                pubsub.subscribe("plc_parameter_setting","plc_parameter_start")
                while running_flag["active"]:
                    start_time = time.time()
                    try:
                        while True:
                            message = pubsub.get_message() #.listen()will stay here till have message ,but get_message() not
                            if message:
                                if message and message.get('type')=='message':
                                    channel = message.get('channel')
                                    data_str = message.get('data','')

                                    if not data_str:
                                        pass
                                    else:
                                        plc_data_new.update(json.loads(data_str))




                                    if channel == "plc_parameter_start":
                                        parameter_dict = json.loads(data_str)
                                        for key_, value_ in parameter_dict.items():
                                            set_client.set(key_, value_)

                                    if channel == "plc_parameter_setting":
                                        parameter_dict = json.loads(data_str)
                                        for key_, value_ in parameter_dict.items():
                                            set_client.set(key_, value_)
                                        #PLC寫入
                                        #PLC讀出
                            if parameter_dict is not None:
                                for key_, value_ in random_signal(parameter_dict).items():
                                    set_client.set(key_, value_)
                            elapse_time = time.time() - start_time
                            time.sleep(max(0.01, loop_time - elapse_time))
                    except (redis.RedisError, Exception):
                        break
                elapse_time = time.time() - start_time
                time.sleep(max(0.01, loop_time - elapse_time))
        except (redis.exceptions.ConnectionError, Exception):
            if not running_flag["active"]:
                break
            time.sleep(1)
        except KeyboardInterrupt:
            break

    set_client.close()
    pubsub_client.close()

    set_pool.disconnect()
    pubsub_pool.disconnect()

def process_random_signal(plc_data_newer: dict,plc_data_older: dict) -> dict:
    process = ''
    result = {}
    if plc_data_newer['process_start_name']:
        if plc_data_newer['process_start_name'] != plc_data_older['process_start_name']:
            plc_data_newer['process_start_time_name'] = time.time()
            plc_data_newer['process_end_time_name'] = 0
            water_pressure_signal(plc_data_newer, True)
            foam_type_signal(plc_data_newer, False)
            wax_type_signal(plc_data_newer, False)
            air_pressure_signal(plc_data_newer, True)

        if time.time() - plc_data_newer['process_start_time_name'] <= 10:
            process = 'preclean'
            water_pressure_signal(plc_data_newer,False)
            foam_type_signal(plc_data_newer,False)
            wax_type_signal(plc_data_newer,False)
            air_pressure_signal(plc_data_newer,True)

        if time.time() - plc_data_newer['process_start_time_name'] <= 20:
            process = 'chemical_soft'
            water_pressure_signal(plc_data_newer,True)
            foam_type_signal(plc_data_newer,True)
            wax_type_signal(plc_data_newer,False)
            air_pressure_signal(plc_data_newer,True)

        if time.time() - plc_data_newer['process_start_time_name'] <= 30:
            process = 'physical_clean'
            water_pressure_signal(plc_data_newer,False)
            foam_type_signal(plc_data_newer,True)
            wax_type_signal(plc_data_newer,False)
            air_pressure_signal(plc_data_newer,True)

        if time.time() - plc_data_newer['process_start_time_name'] <= 40:
            process = 'wax_protect'
            water_pressure_signal(plc_data_newer,False)
            foam_type_signal(plc_data_newer,False)
            wax_type_signal(plc_data_newer,True)
            air_pressure_signal(plc_data_newer,True)

        if time.time() - plc_data_newer['process_start_time_name'] <= 50:
            process = 'dry_air'
            water_pressure_signal(plc_data_newer,True)
            foam_type_signal(plc_data_newer,False)
            wax_type_signal(plc_data_newer,False)
            air_pressure_signal(plc_data_newer,False)

        if time.time() - plc_data_newer['process_start_time_name'] <= 60:
            process = 'standby'
            water_pressure_signal(plc_data_newer,True)
            foam_type_signal(plc_data_newer,False)
            wax_type_signal(plc_data_newer,False)
            air_pressure_signal(plc_data_newer,True)

            plc_data_newer['process_end_time_name'] = time.time()
            plc_data_newer['process_start_name'] = False

    else:
        process = 'standby'
        water_pressure_signal(plc_data_newer, True)
        foam_type_signal(plc_data_newer, False)
        wax_type_signal(plc_data_newer, False)
        air_pressure_signal(plc_data_newer, True)


        water_pressure_base = message.get((redis_name.get('parameter_water_pressure_name')), 0)
        water_pressure = random.uniform(water_pressure_base * 10, water_pressure_base * 20)
        air_pressure_base = message.get((redis_name.get('parameter_air_pressure_name')), 0)
        air_pressure = random.uniform(air_pressure_base * 15, air_pressure_base * 25)

        if message.get((redis_name.get('parameter_foam_type_name'))) == 0:
            foam_type = 'Normal_Foam'
        elif message.get((redis_name.get('parameter_foam_type_name'))) == 1:
            foam_type = 'Super_Foam'
        else:
            foam_type = 'None'

        if message.get((redis_name.get('parameter_wax_type_name'))) == 0:
            wax_type = 'Normal_Wax'
        elif message.get((redis_name.get('parameter_wax_type_name'))) == 1:
            wax_type = 'Super_Wax'
        else:
            wax_type = 'None'

        watchdog = int(time.time())

        random_dist = {
            redis_name.get('water_pressure_name'): water_pressure,
            redis_name.get('foam_type_name'): foam_type,
            redis_name.get('wax_type_name'): wax_type,
            redis_name.get('air_pressure_name'): air_pressure,
            redis_name.get('watchdog_name'): watchdog,
        }
        result.update(message)
        result.update(random_dist)
    return result

def water_pressure_signal(plc_data: dict,zero: bool) -> None:
    if zero:
        plc_data['water_pressure_name'] = 0
        plc_data['water_pressure_used_name'] = False
    else:
        plc_data['water_pressure_name'] = random.uniform((plc_data.get('parameter_water_pressure_name')+1)*10,
                                                                   (plc_data.get('parameter_water_pressure_name')+1)*20)
        plc_data['water_pressure_used_name'] = True

def foam_type_signal(plc_data: dict,used: bool) -> None:
    if plc_data.get('parameter_foam_type_name') == 0:
        foam_type = 'Normal_Foam'
    elif plc_data.get('parameter_foam_type_name') == 1:
        foam_type = 'Super_Foam'
    else:
        foam_type = 'None'
    plc_data['foam_type_name'] = foam_type
    plc_data['foam_type_used_name'] = used

def wax_type_signal(plc_data: dict,used: bool) -> None:
    if plc_data.get('parameter_wax_type_name') == 0:
        wax_type = 'Normal_Wax'
    elif plc_data.get('parameter_wax_type_name') == 1:
        wax_type = 'Super_Wax'
    else:
        wax_type = 'None'
    plc_data['wax_type_name'] = wax_type
    plc_data['wax_type_used_name'] = used

def air_pressure_signal(plc_data: dict,zero: bool) -> None:
    if zero:
        plc_data['air_pressure_name'] = 0
        plc_data['air_pressure_used_name'] = False
    else:
        plc_data['air_pressure_name'] = random.uniform((plc_data.get('parameter_air_pressure_name') + 1) * 15,
                                                                   (plc_data.get('parameter_air_pressure_name') + 1) * 25)
        plc_data['air_pressure_used_name'] = True

def status_signal(plc_data: dict,status: str) -> None:
    if status == 'standby':
        plc_data['standby_status_name'] = True
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status_name'] = False
    elif status == 'preclean':
        plc_data['standby_status_name'] = False
        plc_data['preclean_status_name'] = True
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status'] = False
    elif status == 'chemical_soft':
        plc_data['standby_status_name_name'] = False
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = True
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status_name'] = False
    elif status == 'physical_clean_status':
        plc_data['standby_status_name'] = False
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = True
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status_name'] = False
    elif status == 'wax_protect_status':
        plc_data['standby_status_name'] = False
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = True
        plc_data['dry_air_status_name'] = False
    elif status == 'dry_air_status':
        plc_data['standby_status_name'] = False
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status_name'] = True
    else:
        plc_data['standby_status_name'] = False
        plc_data['preclean_status_name'] = False
        plc_data['chemical_soft_status_name'] = False
        plc_data['physical_clean_status_name'] = False
        plc_data['wax_protect_status_name'] = False
        plc_data['dry_air_status_name'] = False



def watchdog_signal() -> dict:
    return {redis_name.get('watchdog_name'): int(time.time())}

def random_signal(message: dict) -> dict:
    result = {}
    if message is not None:
        water_pressure_base = message.get((redis_name.get('parameter_water_pressure_name')),0)
        water_pressure = random.uniform(water_pressure_base*10,water_pressure_base*20)
        air_pressure_base = message.get((redis_name.get('parameter_air_pressure_name')),0)
        air_pressure = random.uniform(air_pressure_base * 15, air_pressure_base * 25)

        if message.get((redis_name.get('parameter_foam_type_name'))) == 0:
            foam_type = 'Normal_Foam'
        elif message.get((redis_name.get('parameter_foam_type_name'))) == 1:
            foam_type = 'Super_Foam'
        else:
            foam_type = 'None'

        if message.get((redis_name.get('parameter_wax_type_name'))) == 0:
            wax_type = 'Normal_Wax'
        elif message.get((redis_name.get('parameter_wax_type_name'))) == 1:
            wax_type = 'Super_Wax'
        else:
            wax_type = 'None'

        watchdog = int(time.time())

        random_dist = {
            redis_name.get('water_pressure_name'): water_pressure,
            redis_name.get('foam_type_name'): foam_type,
            redis_name.get('wax_type_name'): wax_type,
            redis_name.get('air_pressure_name'): air_pressure,
            redis_name.get('watchdog_name'): watchdog,
        }
        result.update(message)
        result.update(random_dist)
    return result


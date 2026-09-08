import redis
import json
import library.file.config_redis as f_cr
import time
import random
from library.file.config_name import redis_name
import library.redis.redis as r_r

running_flag = {"active": True}
parameter_dict = {}
redis_host, redis_port, redis_password = f_cr.read_redis_config()

def plc_client() -> None:
    global parameter_dict
    while running_flag["active"]:
        try:
            with redis.Redis(host=redis_host, port=int(redis_port), password=redis_password, db=0,
                                 decode_responses=True, socket_connect_timeout=1) as client:
                client.ping()
                with client.pubsub(ignore_subscribe_messages=True) as pubsub:
                    pubsub.subscribe("plc_parameter_setting")
                    while running_flag["active"]:
                        start_time = time.time()
                        try:
                            message = pubsub.get_message() #.listen()will stay here till have message ,but get_message() not
                            if message:
                                parameter_dict = json.loads(message)
                                #PLC寫入
                                #PLC讀出
                            for key, value in random_signal(parameter_dict).items():
                                r_r.set_with_expiry(key, value)
                            elapse_time = time.time() - start_time
                            time.sleep(max(0, (elapse_time)))
                        except (redis.RedisError, Exception):
                            break
        except (redis.exceptions.ConnectionError, Exception):
            if not running_flag["active"]:
                break
            time.sleep(1)
        except KeyboardInterrupt:
            break



def random_signal(message: dict) -> dict:
    water_pressure_base = message.get((redis_name.get('parameter_water_pressure_name')))
    water_pressure = random.uniform(water_pressure_base*10,water_pressure_base*20)
    air_pressure_base = message.get((redis_name.get('parameter_air_pressure_name')))
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

    random_dist = {
        redis_name.get('parameter_water_pressure_name')+redis_name.get('real_data_name'): water_pressure,
        redis_name.get('parameter_foam_type_name') + redis_name.get('real_data_name'): foam_type,
        redis_name.get('parameter_wax_type_name') + redis_name.get('real_data_name'): wax_type,
        redis_name.get('parameter_air_pressure_name') + redis_name.get('real_data_name'): air_pressure,
    }
    message.update(random_dist)
    return message


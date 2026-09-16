import redis, json, time, random
import library.file.config_redis as f_cr
from library.file.config_name import redis_name
from typing import Optional

running_flag = {"active": True}
parameter_dict: Optional[dict] =None
redis_host, redis_port, redis_password = f_cr.read_redis_config()

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

def plc_client() -> None:
    global parameter_dict
    loop_time = 0.1
    while running_flag["active"]:
        try:
            pubsub_client.ping()
            with pubsub_client.pubsub(ignore_subscribe_messages=True) as pubsub:
                pubsub.subscribe("plc_parameter_setting")
                while running_flag["active"]:
                    start_time = time.time()
                    try:
                        message = pubsub.get_message() #.listen()will stay here till have message ,but get_message() not
                        if message and message.get('type')=='message':
                            parameter_dict = json.loads(message['data'])
                            #PLC寫入
                            #PLC讀出
                        if parameter_dict is not None:
                            for key, value in random_signal(parameter_dict).items():
                                set_client.set(key, value)
                        elapse_time = time.time() - start_time
                        time.sleep(max(0.01, loop_time-elapse_time))
                    except (redis.RedisError, Exception):
                        break
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


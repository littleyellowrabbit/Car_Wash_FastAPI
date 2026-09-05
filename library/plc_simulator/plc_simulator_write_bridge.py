import redis
import json
import library.file.config_redis as f_cr
import time

running_flag = {"active": True}
parameter_dict = {}

def plc_client() -> None:
    redis_host, redis_port, redis_password = f_cr.read_redis_config()
    client = redis.Redis(host=redis_host, port=int(redis_port), password=redis_password, db=0, decode_responses=True,socket_connect_timeout=1)
    global parameter_dict
    while running_flag["active"]:
        try:
            client.ping()
            pubsub = client.pubsub()
            pubsub.subscribe("plc_parameter_setting")

            for message in pubsub.listen():
                if not running_flag["active"]:
                    break

                if message["type"] == "message":
                    raw_data = message["data"]
                    try:
                        parameter_dict = json.loads(raw_data)
                    except json.decoder.JSONDecodeError:
                        continue
        except (redis.exceptions.ConnectionError, Exception):
            if not running_flag["active"]:
                break
            time.sleep(1)



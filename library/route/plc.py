import route_format as r_rf
import library.file.config_token as f_ct
import library.redis.redis as r_r
from fastapi import Depends, HTTPException, APIRouter, status, WebSocket, WebSocketDisconnect
from library.file.config_name import redis_name
import library.route.route_format as r_f
import asyncio

plc = APIRouter(prefix="/plc", tags=["plc"])

@plc.post("/set_parameter",status_code=status.HTTP_200_OK)
async def set_parameter(data:r_rf.SetParameter, _ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access), redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        message = (f'{{{redis_name.get('parameter_water_pressure_name')}: {data.water_pressure},'
                   f'{redis_name.get('parameter_wax_type_name')}: {data.wax_type},'
                   f'{redis_name.get('parameter_foam_type_name')}: {data.foam_type},'
                   f'{redis_name.get('parameter_air_pressure_name')}: {data.air_pressure}}}')
        await redis_session.publish("plc_parameter_setting", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@plc.post("/process_start",status_code=status.HTTP_200_OK)
async def process_start(start: bool,redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        message = (f'{{{redis_name.get('parameter_process_start_name')}: {start}}}'
        )
        await redis_session.publish("plc_parameter_start", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@plc.websocket("/real_time_data")
async def websocket_plc(websocket: WebSocket, redis_session = Depends(r_r.get_redis_client)):
    await websocket.accept()

    parameter_water_pressure = redis_name.get('parameter_water_pressure_name')
    parameter_wax_type_name = redis_name.get('parameter_wax_type_name')
    parameter_foam_type_name = redis_name.get('parameter_foam_type_name')
    parameter_air_pressure_name = redis_name.get('parameter_air_pressure_name')

    watchdog = redis_name.get('watchdog_name') + redis_name.get('real_data_name')
    water_pressure = redis_name.get('water_pressure_name')
    wax_type_name = redis_name.get('wax_type_name')
    foam_type_name = redis_name.get('foam_type_name')
    air_pressure_name = redis_name.get('air_pressure_name')

    keys_to_fetch = [
        parameter_water_pressure,
        parameter_wax_type_name,
        parameter_foam_type_name,
        parameter_air_pressure_name,
        watchdog,
        water_pressure,
        wax_type_name,
        foam_type_name,
        air_pressure_name,
    ]
    try:
        while True:
            raw_data = await redis_session.mget(keys_to_fetch)
            raw_dict = {f:v for f,v in zip(keys_to_fetch, raw_data) if v is not None}

            live_data_model = r_f.PLCLiveData(**raw_dict)
            await websocket.send_text(live_data_model.model_dump_json())
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        pass

    finally:
        pass

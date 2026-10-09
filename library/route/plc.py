import json
import library.file.config_token as f_ct
import library.redis.redis as r_r
from fastapi import Depends, HTTPException, APIRouter, status, WebSocket, WebSocketDisconnect
from library.file.config_name import redis_name
import library.route.route_format as r_rf
import asyncio
from library.file.config_plc_simulator_default import PLC_DEFAULT_CACHE
plc_data = PLC_DEFAULT_CACHE.copy()
plc = APIRouter(prefix="/plc", tags=["plc"])

@plc.post("/set_parameter",status_code=status.HTTP_200_OK)
async def set_parameter(data:r_rf.SetParameter, _ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access), redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        message_dict = {redis_name.get('parameter_water_pressure_name'): data.water_pressure,
                   redis_name.get('parameter_wax_type_name'): data.wax_type,
                   redis_name.get('parameter_foam_type_name'): data.foam_type,
                   redis_name.get('parameter_air_pressure_name'): data.air_pressure,
                   }
        message = json.dumps(message_dict)
        await redis_session.publish("plc_parameter_setting", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@plc.post("/process_start",status_code=status.HTTP_200_OK)
async def process_start(data: r_rf.StartProcess,redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        if data.Start_Process:
            trans_value = 1
        else:
            trans_value = 0

        message_dict = {redis_name.get('parameter_process_start_name'): trans_value}
        message = json.dumps(message_dict)
        await redis_session.publish("plc_parameter_start", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))

@plc.post("/process_stop",status_code=status.HTTP_200_OK)
async def process_stop(data: r_rf.StopProcess,redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        if data.Stop_Process:
            trans_value = 0
        else:
            trans_value = 1

        message_dict = {redis_name.get('parameter_process_start_name'): trans_value}
        message = json.dumps(message_dict)
        await redis_session.publish("plc_parameter_start", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


@plc.websocket("/real_time_data")
async def websocket_plc(websocket: WebSocket, redis_session = Depends(r_r.get_redis_client)):
    await websocket.accept()
    keys = plc_data.keys()
    keys_to_fetch = [key for key in keys]
    keys_name = [name.split(':')[-1] for name in keys]
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
            except asyncio.TimeoutError:
                pass

            raw_data = await redis_session.mget(keys_to_fetch)
            raw_dict = {f:v for f,v in zip(keys_name, raw_data) if v is not None}
            #live_data_model = r_rf.PLCLiveData(**raw_dict) #only range/default check
            live_data_model = r_rf.PLCLiveData.model_validate(raw_dict) #have turn type
            await websocket.send_text(live_data_model.model_dump_json())
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        pass

    finally:
        pass

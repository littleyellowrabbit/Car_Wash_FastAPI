import route_format as r_rf
import library.file.config_token as f_ct
import library.redis.redis as r_r
from fastapi import Depends, HTTPException, APIRouter, status

plc = APIRouter(prefix="/plc", tags=["plc"])

@plc.post("/set_parameter",status_code=status.HTTP_200_OK)
async def set_parameter(data:r_rf.SetParameter, _ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access)) -> dict:
    try:
        message = f'{{water_pressure: {data.water_pressure},wax_type: {data.wax_type},foam_type: {data.foam_type},air_pressure: {data.air_pressure}}}'
        await r_r.redis_session.publish("plc_parameter_setting", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
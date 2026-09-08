import route_format as r_rf
import library.file.config_token as f_ct
import library.redis.redis as r_r
from fastapi import Depends, HTTPException, APIRouter, status
from library.file.config_name import redis_name

plc = APIRouter(prefix="/plc", tags=["plc"])

@plc.post("/set_parameter",status_code=status.HTTP_200_OK)
async def set_parameter(data:r_rf.SetParameter, _ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access)) -> dict:
    try:
        message = (f'{{{redis_name.get('parameter_water_pressure_name')}: {data.water_pressure},'
                   f'{redis_name.get('parameter_wax_type_name')}: {data.wax_type},'
                   f'{redis_name.get('parameter_foam_type_name')}: {data.foam_type},'
                   f'{redis_name.get('parameter_air_pressure_name')}: {data.air_pressure}}}')
        await r_r.redis_session.publish("plc_parameter_setting", message)
        return {'states': 'success','detail': f'{message}'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
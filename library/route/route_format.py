from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

_PERMISSION_TUPLE = ('Administrator', 'Engineer', 'Operator')

def permission_trans(permission) -> str:
    if str(permission) not in _PERMISSION_TUPLE:
        return 'Operator'
    else:
        return permission



class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


#account

class AccessUser(Base):
    id: Annotated[int, Field(ge=0)]
    permission: Annotated[str, Field(min_length=1, max_length=15)]
    exp : Annotated[int, Field(ge=0)]

class RefreshUser(Base):
    id: Annotated[int, Field(ge=0)]
    exp: Annotated[int, Field(ge=0)]

class Login(Base):
    name : Annotated[str, Field(min_length=1, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    password : Annotated[str, Field(min_length=6, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]

class LoginResponse(Base):
    id : Annotated[int, Field(ge=0)]
    permission : Annotated[str, Field(min_length=1, max_length=15)]
    exp : Annotated[int, Field(gt=0)]
    access_token : str
    refresh_token : str

class RefreshResponse(Base):
    id : Annotated[int, Field(ge=0)]
    permission : Annotated[str, Field(min_length=1, max_length=15)]
    exp : Annotated[int, Field(gt=0)]
    access_token : str
    refresh_token : str

class AddUser(Base):
    name: Annotated[str, Field(min_length=1, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    password: Annotated[str, Field(min_length=6, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    permission: Annotated[str, Field(min_length=1, max_length=15)]

class DelUser(Base):
    name: Annotated[str, Field(min_length=1, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]


#keyparameter
class SetParameter(Base):
    water_pressure : Annotated[int, Field(ge=0,le=4)]
    wax_type: Annotated[int, Field(ge=0, le=1)]
    foam_type: Annotated[int, Field(ge=0, le=1)]
    air_pressure: Annotated[int, Field(ge=0, le=4)]

#Start process
class StartProcess(Base):
    Start_Process : Annotated[bool, ''] = False

#Stop process
class StopProcess(Base):
    Stop_Process : Annotated[bool, ''] = True



#plc_return
class PLCLiveData(Base):
    parameter_water_pressure: Annotated[int, Field(0,ge=0,le=4)]
    parameter_wax_type: Annotated[int, Field(0,ge=0,le=1)]
    parameter_foam_type: Annotated[int, Field(0,ge=0,le=1)]
    parameter_air_pressure: Annotated[int, Field(0,ge=0,le=4)]
    parameter_process_start: Annotated[bool,'']= False
    water_pressure: Annotated[int, Field(0,ge=-20,le=9999)]
    wax_type: Annotated[str,'']= ''
    foam_type: Annotated[str,'']= ''
    air_pressure: Annotated[int, Field(0,ge=-20,le=9999)]
    water_pressure_used: Annotated[bool,'']= False
    foam_type_used: Annotated[bool,'']= False
    wax_type_used: Annotated[bool,'']= False
    air_pressure_used: Annotated[bool,'']= False
    standby_status: Annotated[bool,'']= False
    preclean_status: Annotated[bool,'']= False
    chemical_soft_status: Annotated[bool,'']= False
    physical_clean_status: Annotated[bool,'']= False
    wax_protect_status: Annotated[bool,'']= False
    dry_air_status: Annotated[bool,'']= False
    process_start: Annotated[bool,'']= False
    process_start_time: Annotated[float,'']= 0
    process_end_time: Annotated[float,'']= 0
    watchdog: Annotated[float,'']= 0

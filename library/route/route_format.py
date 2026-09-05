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



#keyparameter
class SetParameter(Base):
    water_pressure : int = Field(ge=0,le=4)
    wax_type: int = Field(ge=0, le=1)
    foam_type: int = Field(ge=0, le=1)
    air_pressure: int = Field(ge=0, le=4)


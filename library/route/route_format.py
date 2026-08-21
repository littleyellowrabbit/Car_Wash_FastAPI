from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Annotated

_PERMISSION_TUPLE = ('Administrator', 'Engineer', 'Operator')

def permission_trans(permission) -> str:
    if str(permission) not in _PERMISSION_TUPLE:
        return 'Operator'
    else:
        return permission

class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Login(Base):
    name : Annotated[str, Field(min_length=1, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    password : Annotated[str, Field(min_length=6, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]

class CurrentUser(Base):
    id: Annotated[int, Field(ge=0)]
    permission: Annotated[str, Field(min_length=1, max_length=15)]

class LoginResponse(Base):
    id : Annotated[int, Field(ge=0)]
    permission : Annotated[str, Field(min_length=1, max_length=15)]
    exp : Annotated[int, Field(gt=0)]
    access_token : str

class User(Base):
    id : Annotated[int, Field(ge=0)]
    name : Annotated[str, Field(min_length=6, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    password : Annotated[str, Field(min_length=6, max_length=15, pattern=r"^[a-zA-Z0-9]+$")]
    permission : Annotated[str, BeforeValidator(permission_trans), Field(min_length=1, max_length=15)]

from pathlib import Path
from typing import Optional
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status, HTTPException
import library.route.route_format as r_rf
from library.file.config_name import redis_name
import library.redis.redis as r_r

_PRIVATE_KEY : Optional[str] = None
_PUBLIC_KEY : Optional[str] = None
_ALGORITHM = 'RS256'

security_scheme = HTTPBearer()


def initial_token() -> None:
    global _PRIVATE_KEY
    if _PRIVATE_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'private_lofi.pem'
        with open(token_config_path, 'r', encoding='utf-8') as file:
            _PRIVATE_KEY = file.read()

    global _PUBLIC_KEY
    if _PUBLIC_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'public_lofi.pem'
        with open(token_config_path, 'r', encoding='utf-8') as file:
            _PUBLIC_KEY = file.read()

def encode_private_key(user_payload : dict) -> str :
    token = jwt.encode(user_payload, _PRIVATE_KEY, algorithm=_ALGORITHM)
    return token

async def decode_public_key_access(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), redis_session = Depends(r_r.get_redis_client)) -> r_rf.AccessUser:
    token = credentials.credentials
    try:
        #algorithms need multi method so need +'s' and []!!!!!!
        payload = jwt.decode(token, _PUBLIC_KEY, algorithms=[_ALGORITHM])

        #decode first then check token,because if opposite their may hack use loop to try your access key.
        if await r_r.get_value(redis_session,redis_name.get('token_access_black_name') + token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        user_data = r_rf.AccessUser(id = payload.get('id'), permission = payload.get('permission'), exp = payload.get('exp'))
        return user_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

async def decode_public_key_refresh(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), redis_session = Depends(r_r.get_redis_client)) -> r_rf.RefreshUser:
    token = credentials.credentials
    try:
        # decode first then check token,because if opposite their may hack use loop to try your access key.
        # algorithms need multi method so need +'s' and []!!!!!!
        payload = jwt.decode(token, _PUBLIC_KEY, algorithms=[_ALGORITHM])
        user_data = r_rf.RefreshUser(id = payload.get('id'),exp = payload.get('exp'))
        redis_key = redis_name.get('token_refresh_name') + str(user_data.id)
        if await r_r.exists(redis_session, redis_key) and await r_r.get_value(redis_session, redis_key) == token:
            return user_data
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str :
    token = credentials.credentials
    return token

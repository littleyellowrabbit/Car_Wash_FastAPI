from pathlib import Path
from typing import Optional
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, status, HTTPException
import library.route.route_format as r_rf

_PRIVATE_KEY : Optional[str] = None
_PUBLIC_KEY : Optional[str] = None
_ALGORITHM = 'RS256'

security_scheme = HTTPBearer()


def initial_token() -> None:
    global _PRIVATE_KEY
    if _PRIVATE_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'private_tEST.pem'
        with open(token_config_path, 'r', encoding='utf-8') as file:
            _PRIVATE_KEY = file.read()

    global _PUBLIC_KEY
    if _PUBLIC_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'public_tEST.pem'
        with open(token_config_path, 'r', encoding='utf-8') as file:
            _PUBLIC_KEY = file.read()

def encode_private_key(user_payload : dict) -> str :
    encode_result = jwt.encode(user_payload, _PRIVATE_KEY, algorithm=_ALGORITHM)
    return encode_result

def decode_public_key(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> r_rf.CurrentUser:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, _PUBLIC_KEY, algorithm=_ALGORITHM)
        user_data = r_rf.CurrentUser(id = payload.get('id'), permission = payload.get('permission'))
        return user_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str :
    token = credentials.credentials
    return token
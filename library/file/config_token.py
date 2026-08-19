from pathlib import Path
from typing import Optional
import jwt

_PRIVATE_KEY : Optional[str] = None
_PUBLIC_KEY : Optional[str] = None
_ALGORITHM = 'RS256'

def encode_private_key(user_payload : dict) -> str :
    global _PRIVATE_KEY
    if _PRIVATE_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'private_tEST.pem'
        with open(token_config_path,'r',encoding='utf-8') as file:
            _PRIVATE_KEY = file.read()
    encode_result = jwt.encode(user_payload, _PRIVATE_KEY, algorithm=_ALGORITHM)
    return encode_result

def decode_public_key() -> str:
    global _PUBLIC_KEY
    if _PUBLIC_KEY is None:
        base_path = Path(__file__).resolve().parent.parent.parent
        token_config_path = base_path / 'config' / 'public_tEST.pem'
        with open(token_config_path,'r',encoding='utf-8') as file:
            _PUBLIC_KEY = file.read()
    return _PUBLIC_KEY



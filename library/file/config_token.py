from pathlib import Path

base_path = Path(__file__).resolve().parent.parent.parent

def read_private_key() -> str:
    token_config_path = base_path / 'config' / 'private_tEST.pem'
    with open(token_config_path,'r') as file:
        return file.read()

PRIVATE_KEY : str = read_private_key()

def read_public_key() -> str:
    token_config_path = base_path / 'config' / 'public_tEST.pem'
    with open(token_config_path,'r') as file:
        return file.read()
PUBLIC_KEY : str = read_public_key()


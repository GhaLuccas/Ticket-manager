from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

from ticket_manager.settings import Settings

pwd_hash = PasswordHash.recommended()
settings = Settings()


def hash_password(pwd: str):
    return pwd_hash.hash(pwd)


def verify_password(clean_pwd: str, hash_pwd: str) -> bool:
    return pwd_hash.verify(clean_pwd, hash_pwd)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

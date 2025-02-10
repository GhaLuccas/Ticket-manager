from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select

from ticket_manager.database import session_db
from ticket_manager.models import Manager
from ticket_manager.settings import Settings

pwd_hash = PasswordHash.recommended()
settings = Settings()

login_required = OAuth2PasswordBearer(tokenUrl='/auth/token')


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


def get_current_user(
    db: session_db,
    token: str = Depends(login_required)
) -> Manager:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.execute(
        select(Manager).where(Manager.username == username)
    ).scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

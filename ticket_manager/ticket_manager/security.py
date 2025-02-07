from typing import Annotated

from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from ticket_manager.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
pwd_hash = PasswordHash.recommended()


def hash_password(pwd: str):
    return pwd_hash.hash(pwd)


def verify_password(clean_pwd: str, hash_pwd: str) -> bool:
    return pwd_hash.verify(clean_pwd, hash_pwd)

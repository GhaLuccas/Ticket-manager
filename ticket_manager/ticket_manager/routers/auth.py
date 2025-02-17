from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from ticket_manager.database import session_db
from ticket_manager.models import Manager
from ticket_manager.schema import Token
from ticket_manager.security import create_access_token, verify_password

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/token', response_model=Token)
def login_token(
    db: session_db,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.scalar(
        select(Manager).where(Manager.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="username or password is wrong"
            )
    else:
        token = create_access_token(data={'sub': user.username})
        return {'access_token': token, 'token_type': 'Bearer'}

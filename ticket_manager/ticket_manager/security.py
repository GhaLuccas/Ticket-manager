from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Manager

SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(request: Request, db: SessionDep):
    user_id = request.cookies.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail='not authenticaded')

    userdb = db.query(Manager).filter(Manager.id == user_id).first()
    user = {
        'username': userdb.username,
        'id': userdb.id
    }

    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    return user

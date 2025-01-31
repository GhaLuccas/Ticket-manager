from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Manager
from ticket_manager.schema import UserManagerSchema

SessionDep = Annotated[Session, Depends(get_session)]


users_router = APIRouter(prefix='/users', tags=['users'])


# OK
@users_router.post('/', status_code=201)
def create_user(user: UserManagerSchema, session: SessionDep):

    user_manager = Manager(
        username=user.username,
        password=user.password,
    )
    session.add(user_manager)
    session.commit()
    session.refresh(user_manager)
    return user_manager

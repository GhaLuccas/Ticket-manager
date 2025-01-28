from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Manager
from ticket_manager.schema import UserManager

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]


@app.get('/')
def hello():
    return {'message': 'hello :)'}


@app.post('/create')
def create_user(user: UserManager, session: SessionDep):

    user_manager = Manager(
        username=user.username,
        password=user.passwordl,
    )
    session.add(user_manager)
    session.commit()
    session.refresh(user_manager)
    return user_manager

from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.routers import auth, clients, users

app = FastAPI()
app.include_router(users.users_router)
app.include_router(clients.clients_router)
app.include_router(auth.auth_router)


SessionDep = Annotated[Session, Depends(get_session)]

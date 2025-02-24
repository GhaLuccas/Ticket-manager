from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ticket_manager.settings import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


session_db = Annotated[Session, Depends(get_session)]

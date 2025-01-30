from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.schema import Client

SessionDep = Annotated[Session, Depends(get_session)]

clients_router = APIRouter(prefix='clients', tags=['clients'])


@clients_router.post('/', status_code=201)
def create_client(client: Client, session: SessionDep):
    company = client.company if client.company else "Não cadastrado"
    phone = client.phone if client.phone else "Não cadastrado"

    client_model = Client(
        name=client.name,
        company_name=company,
        phone=phone
    )

    session.add(client_model)
    session.commit()

    session.refresh(client_model)

    return client_model

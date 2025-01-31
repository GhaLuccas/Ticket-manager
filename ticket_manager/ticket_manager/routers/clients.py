from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Client
from ticket_manager.schema import ClientSchema

SessionDep = Annotated[Session, Depends(get_session)]

clients_router = APIRouter(prefix='/clients', tags=['clients'])


@clients_router.post('/', status_code=201)
def create_client(client: ClientSchema, session: SessionDep):
    company = client.company_name if client.company_name else "Não cadastrado"
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


@clients_router.get('/', status_code=200)
def search_clients(session: SessionDep, search_term: str):
    query = select(Client).where(
        or_(
            Client.name.ilike(f"%{search_term}%"),
            Client.company_name.ilike(f"%{search_term}%")
        )
    )
    clients = session.scalars(query).all()
    return clients

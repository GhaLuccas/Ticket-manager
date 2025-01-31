from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Client
from ticket_manager.schema import ClientSchema

SessionDep = Annotated[Session, Depends(get_session)]

clients_router = APIRouter(prefix='/clients', tags=['clients'])


@clients_router.post("/", status_code=201)
def create_client(client: ClientSchema, session: SessionDep):
    client_model = Client(
        name=client.name,
        company_name=client.company_name or "Não cadastrado",
        phone=client.phone or "Não cadastrado",
    )
    session.add(client_model)
    session.commit()
    session.refresh(client_model)
    return client_model


@clients_router.put('/{client_id}', status_code=200)
def update_client(
    client_id: int,
    client: ClientSchema,
    session: SessionDep,
):
    existing_client = session.get(Client, client_id)

    if not existing_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    existing_client.name = client.name or existing_client.name
    existing_client.company_name = (
        client.company_name or existing_client.company_name
        )
    existing_client.phone = client.phone or existing_client.phone

    session.commit()
    session.refresh(existing_client)

    return existing_client


@clients_router.get('/', status_code=200)
def search_clients(session: SessionDep, search_term: str):
    query = select(Client).where(
        or_(
            Client.name.ilike(f"%{search_term}%"),
            Client.company_name.ilike(f"%{search_term}%")
        )
    )
    clients = session.scalars(query).all()
    if not clients:
        raise HTTPException(status_code=404,
                            detail="Nenhum cliente encontrado")

    return clients


@clients_router.delete('/{client_id}', status_code=204)
def delete_client(session: SessionDep, client_id: int):
    client = session.get(Client, client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(client)
    session.commit()

    return ''

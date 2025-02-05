from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ticket_manager.database import get_session
from ticket_manager.models import Client
from ticket_manager.schema import ClientList, ClientPublicShcema, ClientSchema

SessionDep = Annotated[Session, Depends(get_session)]

clients_router = APIRouter(prefix='/clients', tags=['clients'])


@clients_router.post(
    "/",
    status_code=201,
    response_model=ClientPublicShcema
    )
def create_client(client: ClientSchema, session: SessionDep):
    new_client = Client(
        name=client.name,
        company_name=client.company_name or "Não cadastrado",
        phone=client.phone or "Não cadastrado",
    )
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return {
        "id": new_client.id,
        "name": new_client.name,
        "company_name": new_client.company_name,
        "phone": new_client.phone
            }


@clients_router.get(
    '/{user_id}',
    status_code=200,
    response_model=ClientPublicShcema,
    )
def get_cllient(client_id: int, session: SessionDep):
    client_query = session.get(Client, client_id)
    if client_query:
        return {
            "id": client_query.id,
            "name": client_query.name,
            "company_name": client_query.company_name,
            "phone": client_query.phone
                }
    else:
        raise HTTPException(
            status_code=404,
            detail="Cliente não foi encontrado")


@clients_router.put(
    '/{client_id}',
    status_code=200,
    response_model=ClientSchema
    )
def update_client(
    client_id: int,
    client: ClientSchema,
    session: SessionDep,
):
    existing_client = session.get(Client, client_id)

    if not existing_client:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado")

    existing_client.name = client.name or existing_client.name
    existing_client.company_name = (
        client.company_name or existing_client.company_name
        )
    existing_client.phone = client.phone or existing_client.phone

    session.commit()
    session.refresh(existing_client)

    return {
        "name": existing_client.name,
        "company_name": existing_client.company_name,
        "phone": existing_client.phone
            }


@clients_router.get(
    '/',
    status_code=200,
    response_model=ClientList
    )
def search_clients(session: SessionDep, search_term: str | None = None):

    if search_term:
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

        client_list = [
            ClientPublicShcema.model_validate(client) for client in clients
            ]
        return {'clientlist': client_list}
    else:
        clients = session.query(Client).all()
        client_list = [
            ClientPublicShcema.model_validate(client) for client in clients
            ]
        return {'clientlist': client_list}


@clients_router.delete('/{client_id}', status_code=204)
def delete_client(session: SessionDep, client_id: int):
    client = session.get(Client, client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    session.delete(client)
    session.commit()

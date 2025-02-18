
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select

from ticket_manager.database import session_db
from ticket_manager.models import Client
from ticket_manager.schema import ClientList, ClientPublic, ClientSchema
from ticket_manager.security import login_required
from ticket_manager.services.clients_services import (
    get_client_by_id,
    parse_client,
    parse_client_public,
)

clients_router = APIRouter(prefix='/clients', tags=['clients'])


@clients_router.post(
    "/",
    status_code=201,
    response_model=ClientPublic
    )
def create_client(
    client: ClientSchema,
    session: session_db,
    loged_user=Depends(login_required)
    ):
    new_client = Client(
        name=client.name,
        company_name=client.company_name or "Não cadastrado",
        phone=client.phone or "Não cadastrado",
    )
    session.add(new_client)
    session.commit()
    session.refresh(new_client)

    return parse_client_public(new_client)


@clients_router.get(
    '/{user_id}',
    status_code=200,
    response_model=ClientPublic
    )
def get_client(
    client_id: int,
    session: session_db,
    loged_user=Depends(login_required)
    ):
    client_query = get_client_by_id(session, client_id)
    return parse_client_public(client_query)


@clients_router.put(
    '/{client_id}',
    status_code=200,
    response_model=ClientSchema
    )
def update_client(
    client_id: int,
    client: ClientSchema,
    session: session_db,
    loged_user=Depends(login_required)
):
    existing_client = get_client_by_id(session, client_id)

    if not any([client.name, client.company_name, client.phone]):
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided for update"
            )

    existing_client.name = client.name or existing_client.name
    existing_client.company_name = (
        client.company_name or existing_client.company_name
        )
    existing_client.phone = client.phone or existing_client.phone

    session.commit()
    session.refresh(existing_client)

    return parse_client(existing_client)


@clients_router.get(
    '/',
    status_code=200,
    response_model=ClientList
    )
def search_clients(
    session: session_db,
    search_term: str | None = None,
    loged_user=Depends(login_required)
    ):

    if search_term:
        query = select(Client).where(
            or_(
                Client.name.ilike(f"%{search_term}%"),
                Client.company_name.ilike(f"%{search_term}%")
            )
        )
        clients = session.scalars(query).all()
        if not clients:
            raise HTTPException(
                status_code=404,
                detail="Nenhum cliente encontrado"
                )
        client_list = [
            ClientPublic.model_validate(client) for client in clients
            ]
        return {'clientlist': client_list}
    else:
        clients = session.query(Client).all()
        client_list = [
            ClientPublic.model_validate(client) for client in clients
            ]
        return {'clientlist': client_list}


@clients_router.delete('/{client_id}', status_code=204)
def delete_client(
    session: session_db,
    client_id: int,
    logged_user=Depends(login_required),
):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    session.delete(client)
    session.commit()

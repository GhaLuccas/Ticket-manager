from fastapi import HTTPException

from ticket_manager.database import session_db
from ticket_manager.models import Client


def get_client_by_id(db: session_db, client_id=int):
    client = db.query(Client).filter(
        Client.id == client_id
    ).first()

    if client:
        return client
    else:
        raise HTTPException(
            status_code=404,
            detail='Not found',
            )


def parse_client_public(client):
    return {
            "id": client.id,
            "name": client.name,
            "company_name": client.company_name,
            "phone": client.phone
                }


def parse_client(client):
    return {
            "name": client.name,
            "company_name": client.company_name,
            "phone": client.phone
                }

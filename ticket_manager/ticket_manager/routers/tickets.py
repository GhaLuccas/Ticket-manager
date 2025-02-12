
from fastapi import APIRouter, Depends, HTTPException

from ticket_manager.database import session_db
from ticket_manager.models import Client, Manager, Ticket
from ticket_manager.schema import TicketCreateSchema, TicketSchema
from ticket_manager.security import login_required

ticket_router = APIRouter(prefix='/tickets', tags=['tickets'])


@ticket_router.post('/', response_model=TicketSchema)
def create_ticket(
    ticket_data: TicketCreateSchema,
    db: session_db,
    current_user: Manager = Depends(login_required)
):
    client = db.query(Client).filter(
        Client.id == ticket_data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    new_ticket = Ticket(
        author_id=current_user.id,
        client_id=client.id,
        problem=ticket_data.problem,
        solution=ticket_data.solution
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from ticket_manager.database import session_db
from ticket_manager.models import Client, Manager, Ticket, TicketState
from ticket_manager.schema import (
    ClientPublic,
    TicketCreateSchema,
    TicketListSchema,
    TicketSchema,
    TicketUpdateSchema,
    UserPublicSchema,
)
from ticket_manager.security import login_required
from ticket_manager.services.ticket_services import (
    authorize_ticket_owner,
    get_ticket_or_404,
)

ticket_router = APIRouter(prefix='/tickets', tags=['tickets'])


@ticket_router.get('/', response_model=TicketListSchema)
def get_all_tickets(
    db: session_db,
    search_term: str = Query(None, description="Termo de pesquisa"),
    state: TicketState = Query(None, description="Filtrar por estado"),
    logged_user: Manager = Depends(login_required)
):
    query = db.query(Ticket).options(joinedload(Ticket.client))

    # Filtra por termo de pesquisa (se fornecido)
    if search_term:
        query = query.join(Client).filter(
            or_(
                Client.name.ilike(f'%{search_term}%'),
                Client.company_name.ilike(f'%{search_term}%')
            )
        )

    # Filtra por estado (se fornecido)
    if state:
        query = query.filter(Ticket.state == state)

    # Ordena os tickets pelos mais recentes primeiro
    query = query.order_by(Ticket.created_at.desc())

    tickets = query.all()

    ticket_list = [
        TicketSchema(
            id=ticket.id,
            author=UserPublicSchema(
                id=ticket.author.id, username=ticket.author.username
            ),
            client=ClientPublic(
                id=ticket.client.id,
                name=ticket.client.name,
                company_name=ticket.client.company_name,
                phone=ticket.client.phone
            ),
            problem=ticket.problem,
            solution=ticket.solution,
            state=ticket.state,
            created_at=ticket.created_at,
            resolved_at=ticket.resolved_at
        )
        for ticket in tickets
    ]

    return TicketListSchema(ticket_list=ticket_list)


@ticket_router.post('/', response_model=TicketSchema)
def create_ticket(
    form: TicketCreateSchema,
    db: session_db,
    logged_user: Manager = Depends(login_required)
):
    client = db.query(Client).filter(Client.id == form.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    new_ticket = Ticket(
        author_id=logged_user.id,
        client_id=client.id,
        problem=form.problem,
        solution=form.solution
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@ticket_router.put('/{ticket_id}', response_model=TicketSchema)
def update_ticket(
    ticket_id: int,
    form: TicketUpdateSchema,
    db: session_db,
    logged_user: Manager = Depends(login_required),
):
    existing_ticket = get_ticket_or_404(db, ticket_id)
    authorize_ticket_owner(existing_ticket, logged_user)

    if form.problem is not None:
        existing_ticket.problem = form.problem
    if form.solution is not None:
        existing_ticket.solution = form.solution
    if form.state is not None:
        existing_ticket.state = form.state

    db.commit()
    db.refresh(existing_ticket)

    return existing_ticket


@ticket_router.get('/{ticket_id}', response_model=TicketSchema)
def get_ticket_by_id(
    ticket_id: int,
    db: session_db,
    logged_user: Manager = Depends(login_required)
):
    ticket = get_ticket_or_404(db, ticket_id)
    return ticket


@ticket_router.delete('/{ticket_id}')
def delete_ticket_by_id(
    ticket_id: int,
    db: session_db,
    logged_user: Manager = Depends(login_required)
):
    ticket = get_ticket_or_404(db, ticket_id)
    authorize_ticket_owner(ticket, logged_user)

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}

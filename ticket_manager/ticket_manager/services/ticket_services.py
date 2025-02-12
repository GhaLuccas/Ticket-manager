from fastapi import HTTPException
from sqlalchemy.orm import Session

from ticket_manager.models import Manager, Ticket


def get_ticket_or_404(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


def authorize_ticket_owner(ticket: Ticket, user: Manager):
    if ticket.author_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the ticket creator can modify it"
        )

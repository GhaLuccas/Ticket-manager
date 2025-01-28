from datetime import datetime

from pydantic import BaseModel

from ticket_manager.models import TicketState


class UserManager(BaseModel):
    id: int
    username: str
    password: str


class Client(BaseModel):
    id: int
    name: str
    company_name: str | None
    phone: str | None


class Ticket(BaseModel):
    id: int
    author: UserManager
    client: Client
    problem: str
    solution: str | None
    state: TicketState
    created_at: datetime = datetime.now()
    resolved_at: datetime | None = None


class TicketList(BaseModel):
    ticket_list: list[Ticket]

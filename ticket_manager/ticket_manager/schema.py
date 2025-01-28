from datetime import datetime

from pydantic import Basemodel

from ticket_manager.models import TicketState


class UserManager(Basemodel):
    id: int
    username: str
    password: str


class Client(Basemodel):
    id: int
    name: str
    company_name: str | None
    phone: str | None


class Ticket(Basemodel):
    id: int
    author: UserManager
    client: Client
    problem: str
    solution: str | None
    state: TicketState
    created_at: datetime = datetime.now()
    resolved_at: datetime | None = None


class TicketList(Basemodel):
    ticket_list: list[Ticket]

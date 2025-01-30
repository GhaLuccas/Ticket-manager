from datetime import datetime

from pydantic import BaseModel, Field

from ticket_manager.models import TicketState


class UserManager(BaseModel):
    username: str
    password: str


class Client(BaseModel):
    name: str
    company: str | None = Field(default="Não cadastrado")
    phone: str | None = Field(default="Não cadastrado")


class Ticket(BaseModel):
    author: UserManager
    client: Client
    problem: str
    solution: str | None
    state: TicketState
    created_at: datetime = datetime.now()
    resolved_at: datetime | None = None


class TicketList(BaseModel):
    ticket_list: list[Ticket]

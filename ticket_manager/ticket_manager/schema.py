from datetime import datetime

from pydantic import BaseModel, Field

from ticket_manager.models import TicketState


class UserManagerSchema(BaseModel):
    username: str
    password: str


class ClientSchema(BaseModel):
    name: str
    company_name: str | None = Field(default="Não cadastrado")
    phone: str | None = Field(default="Não cadastrado")


class TicketSchema(BaseModel):
    author: UserManagerSchema
    client: ClientSchema
    problem: str
    solution: str | None
    state: TicketState
    created_at: datetime = datetime.now()
    resolved_at: datetime | None = None


class TicketListSchema(BaseModel):
    ticket_list: list[TicketSchema]

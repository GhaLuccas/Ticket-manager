from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

mapper_registry = registry()


@mapper_registry.mapped_as_dataclass
class Manager:
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
        )


@mapper_registry.mapped_as_dataclass
class ClientModel:
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True
        )
    name: Mapped[str | None]
    company_name: Mapped[str]
    phone: Mapped[str | None]


class TicketState(str, Enum):
    done = 'done'
    to_fix = 'To-fix'
    on_going = 'on_going'


@mapper_registry.mapped_as_dataclass
class TicketModel:
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    problem: Mapped[str]
    solution: Mapped[str | None]
    state: Mapped[TicketState]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
        )
    resolved_at: Mapped[datetime | None]

from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

mapper_registry = registry()


@mapper_registry.mapped_as_dataclass
class Manager:
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), default=datetime.utcnow
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="author")


@mapper_registry.mapped_as_dataclass
class Client:
    """Represents a client who has tickets."""
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    company_name: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="client")


class TicketState(str, Enum):
    done = 'done'
    to_fix = 'To-fix'
    on_going = 'on_going'


@mapper_registry.mapped_as_dataclass
class Ticket:
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    problem: Mapped[str] = mapped_column(unique=False)
    solution: Mapped[str] = mapped_column(unique=False)
    state: Mapped[TicketState] = mapped_column(SQLAlchemyEnum(TicketState))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), default=datetime.utcnow
    )
    resolved_at: Mapped[datetime | None]

    author: Mapped["Manager"] = relationship(back_populates="tickets")
    client: Mapped["Client"] = relationship(back_populates="tickets")

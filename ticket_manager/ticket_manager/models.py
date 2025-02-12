from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
)

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

    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="author", init=False
        )


@mapper_registry.mapped_as_dataclass
class Client:
    """Represents a client who has tickets."""
    __tablename__ = "clients"
    __table_args__ = (
        Index('idx_company_name', 'company_name'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    company_name: Mapped[str] = mapped_column(unique=False)
    phone: Mapped[str] = mapped_column(unique=False)

    tickets: Mapped[List["Ticket"]] = relationship(
        back_populates="client", init=False
        )


class TicketState(str, Enum):
    done = 'done'
    to_fix = 'To-fix'
    on_going = 'on_going'


@mapper_registry.mapped_as_dataclass
class Ticket:
    __tablename__ = "tickets"
    __table_args__ = (Index('idx_client_id', 'client_id'),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    problem: Mapped[str] = mapped_column(unique=False)

    author: Mapped["Manager"] = relationship(
        back_populates="tickets",
        init=False)
    client: Mapped["Client"] = relationship(
        back_populates="tickets",
        init=False)

    resolved_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    solution: Mapped[Optional[str]] = mapped_column(default=None)
    state: Mapped[TicketState] = mapped_column(
        SQLAlchemyEnum(TicketState),
        init=False,
        default=TicketState.on_going
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

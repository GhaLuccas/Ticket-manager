from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Index, func
from sqlalchemy.orm import (
    Mapped,
    Session,
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
    company_name: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)

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
    __table_args__ = (
        Index('idx_client_id', 'client_id'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    problem: Mapped[str] = mapped_column(unique=False)
    solution: Mapped[str] = mapped_column(unique=False)
    state: Mapped[TicketState] = mapped_column(SQLAlchemyEnum(TicketState))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), default=datetime.utcnow
    )
    resolved_at: Mapped[Optional[datetime]]

    author: Mapped["Manager"] = relationship(back_populates="tickets")
    client: Mapped["Client"] = relationship(back_populates="tickets")

    @classmethod
    def get_tickets_by_client(
        cls, session: Session, client_id: int
        ) -> List["Ticket"]:
        return session.query(cls).filter_by(client_id=client_id).all()

    @classmethod
    def get_tickets_by_company(
        cls, session: Session, company_name: str
        ) -> List["Ticket"]:
        return session.query(cls).join(Client).filter(
            Client.company_name == company_name).all(
            )

"""Adicionar cascade ao relacionamento Client-Ticket

Revision ID: 00b1c6dda137
Revises: 2332137b4887
Create Date: 2025-02-18 19:20:29.184440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00b1c6dda137'
down_revision: Union[str, None] = '2332137b4887'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

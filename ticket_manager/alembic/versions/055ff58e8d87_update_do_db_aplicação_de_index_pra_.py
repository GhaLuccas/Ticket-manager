"""update do db , aplicação de index pra query

Revision ID: 055ff58e8d87
Revises: f26d35767aa2
Create Date: 2025-01-31 10:18:18.073192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '055ff58e8d87'
down_revision: Union[str, None] = 'f26d35767aa2'
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

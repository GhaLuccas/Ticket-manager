"""tenho que estudar sqlalchemy

Revision ID: 53602843e443
Revises: 0e1272288fcf
Create Date: 2025-02-02 16:27:27.392459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53602843e443'
down_revision: Union[str, None] = '0e1272288fcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_client_id', table_name='tickets')
    op.drop_table('tickets')
    op.drop_table('managers')
    op.drop_index('idx_company_name', table_name='clients')
    op.drop_table('clients')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('company_name', sa.VARCHAR(), nullable=False),
    sa.Column('phone', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_company_name', 'clients', ['company_name'], unique=False)
    op.create_table('managers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tickets',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('author_id', sa.INTEGER(), nullable=False),
    sa.Column('client_id', sa.INTEGER(), nullable=False),
    sa.Column('problem', sa.VARCHAR(), nullable=False),
    sa.Column('solution', sa.VARCHAR(), nullable=False),
    sa.Column('state', sa.VARCHAR(length=8), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('resolved_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['managers.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_client_id', 'tickets', ['client_id'], unique=False)
    # ### end Alembic commands ###

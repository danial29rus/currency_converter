"""Initial10

Revision ID: e668640a62f2
Revises: 
Create Date: 2023-04-22 00:03:56.541548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e668640a62f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency_code', sa.String(length=3), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currency_rates_id'), 'currency_rates', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_currency_rates_id'), table_name='currency_rates')
    op.drop_table('currency_rates')
    # ### end Alembic commands ###

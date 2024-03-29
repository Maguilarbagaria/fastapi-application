"""phone number

Revision ID: 521db78c7eb0
Revises: f7194d646bc6
Create Date: 2023-01-07 19:58:26.291698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521db78c7eb0'
down_revision = 'f7194d646bc6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###

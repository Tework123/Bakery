"""empty message

Revision ID: 29cc81e1f4b2
Revises: 
Create Date: 2023-07-10 08:41:38.848428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29cc81e1f4b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=40), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_token'), ['token'], unique=True)
        batch_op.create_unique_constraint(None, ['phone'])
        batch_op.drop_column('name')
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_index(batch_op.f('ix_users_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')

    # ### end Alembic commands ###

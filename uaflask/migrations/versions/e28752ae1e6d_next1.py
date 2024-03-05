"""next1

Revision ID: e28752ae1e6d
Revises: 0be4241746dd
Create Date: 2024-03-05 18:02:11.118456

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e28752ae1e6d'
down_revision = '0be4241746dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=postgresql.BYTEA(),
               type_=sa.VARCHAR(length=30),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)

    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(length=30),
               type_=postgresql.BYTEA(),
               nullable=False)

    # ### end Alembic commands ###
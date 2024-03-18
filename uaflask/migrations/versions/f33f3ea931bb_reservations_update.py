"""reservations update

Revision ID: f33f3ea931bb
Revises: f3ef46f67144
Create Date: 2024-03-15 14:46:45.969253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f33f3ea931bb'
down_revision = 'f3ef46f67144'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['title'])

    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('post_id')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
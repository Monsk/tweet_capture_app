"""empty message

Revision ID: 5e8e93c10ac8
Revises: 964c932b8bfc
Create Date: 2017-06-25 15:17:11.698839

"""

# revision identifiers, used by Alembic.
revision = '5e8e93c10ac8'
down_revision = '964c932b8bfc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('computedData',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataTitle', sa.String(), nullable=True),
    sa.Column('jsonData', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('computedData')
    ### end Alembic commands ###

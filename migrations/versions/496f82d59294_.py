"""empty message

Revision ID: 496f82d59294
Revises: None
Create Date: 2016-10-31 23:09:45.629606

"""

# revision identifiers, used by Alembic.
revision = '496f82d59294'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tweet_id', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('url_link', sa.String(), nullable=True),
    sa.Column('retweet_count', sa.Integer(), nullable=True),
    sa.Column('retweet_text', sa.String(), nullable=True),
    sa.Column('lang', sa.String(), nullable=True),
    sa.Column('time_zone', sa.String(), nullable=True),
    sa.Column('source', sa.String(), nullable=True),
    sa.Column('user_location', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('user_screen_name', sa.String(), nullable=True),
    sa.Column('source_user_id', sa.String(), nullable=True),
    sa.Column('source_user_screen_name', sa.String(), nullable=True),
    sa.Column('recorded_at', sa.DateTime(), nullable=True),
    sa.Column('occurred_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweet')
    ### end Alembic commands ###

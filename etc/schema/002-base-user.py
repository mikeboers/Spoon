import datetime

import sqlalchemy as sa
from alembic import op


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    users = sa.Table('users', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String, nullable=False),
        sa.Column('email', sa.String),
        sa.Column('password_hash', sa.String),
    )
    users.create()






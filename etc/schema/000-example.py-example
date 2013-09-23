import datetime

import sqlalchemy as sa
from alembic import op


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    services = sa.Table('services', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('cron_spec', sa.String),
        sa.Column('url_to_monitor', sa.String),
    )
    services.create()

    heartbeats = sa.Table('heartbeats', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('service_id', sa.Integer, sa.ForeignKey('services.id')),
        sa.Column('time', sa.DateTime, nullable=False),
        sa.Column('remote_addr', sa.String, nullable=False),
        sa.Column('remote_name', sa.String, nullable=False),
    )
    heartbeats.create()





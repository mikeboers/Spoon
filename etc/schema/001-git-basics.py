import datetime

import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    groups = sa.Table('groups', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )
    groups.create()

    repos = sa.Table('repos', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')),
        sa.Column('name', sa.String, nullable=False),
    )
    repos.create()





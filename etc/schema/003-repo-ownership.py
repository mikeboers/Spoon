import datetime

import sqlalchemy as sa

def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()


    memberships = sa.Table('group_memberships', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    memberships.create()


    col = sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    col.create(meta.tables['repos'])


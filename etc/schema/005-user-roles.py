import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    roles = sa.Column('roles', sa.String)
    roles.create(meta.tables['users'])

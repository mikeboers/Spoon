import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    admin = sa.Column('is_admin', sa.Boolean)
    admin.create(meta.tables['memberships'])

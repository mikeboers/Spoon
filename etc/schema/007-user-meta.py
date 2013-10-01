import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    sa.Column('description', sa.String).create(meta.tables['users'])
    sa.Column('display_name', sa.String).create(meta.tables['users'])
    sa.Column('display_name', sa.String).create(meta.tables['repos'])
    sa.Column('display_name', sa.String).create(meta.tables['groups'])
    sa.Column('email', sa.String).create(meta.tables['repos'])
    sa.Column('email', sa.String).create(meta.tables['groups'])


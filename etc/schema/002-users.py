import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    users = sa.Table('users', meta,

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String),
        sa.Column('password_hash', sa.BLOB),

        sa.Column('is_admin', sa.Boolean, nullable=False, server_default=sa.text('0')),

        # This is nullable; users don't have to have a home.
        sa.Column('home_id', sa.Integer, sa.ForeignKey('repos.id'))

    )
    users.create()






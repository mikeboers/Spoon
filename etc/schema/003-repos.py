import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()


    repos = sa.Table('repos', meta,

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id')),
        sa.Column('name', sa.String, nullable=False),

        # For display info a blank string will stand for no data.
        sa.Column('display_name', sa.String, nullable=False, server_default=''),
        sa.Column('description', sa.String, nullable=False, server_default=''),
        sa.Column('url', sa.String, nullable=False, server_default=''),
        sa.Column('email', sa.String, nullable=False, server_default=''),

        sa.Column('is_public', sa.Boolean, nullable=False, server_default=sa.text('0')),

    )
    repos.create()


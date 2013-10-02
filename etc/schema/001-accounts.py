import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()


    accounts = sa.Table('accounts', meta,

        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),

        sa.Column('is_group', sa.Boolean, nullable=False, server_default=sa.text('0')),
        
        # Only for users, ergo nullable.
        sa.Column('password_hash', sa.String),
        sa.Column('roles', sa.String),

        # For the display info, a blank string will stand for no data.
        sa.Column('display_name', sa.String, nullable=False, server_default=''),
        sa.Column('description', sa.String, nullable=False, server_default=''),
        sa.Column('url', sa.String, nullable=False, server_default=''),
        sa.Column('email', sa.String, nullable=False, server_default=''),

        sa.Column('is_public', sa.Boolean, nullable=False, server_default=sa.text('0')),

    )
    accounts.create()

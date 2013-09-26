import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()


    memberships = sa.Table('memberships', meta,
    
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),

        sa.Column('is_public', sa.Integer, nullable=False, server_default=sa.text('1'))
    )

    memberships.create()



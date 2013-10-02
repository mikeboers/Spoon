import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()


    group_memberships = sa.Table('group_memberships', meta,
    
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('group_id', sa.Integer, sa.ForeignKey('accounts.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('accounts.id'), nullable=False),

        sa.Column('is_public', sa.Integer, nullable=False, server_default=sa.text('1')),

        # Should these be roles instead?
        sa.Column('is_admin', sa.Integer, nullable=False, server_default=sa.text('1')),
        sa.Column('is_writer', sa.Integer, nullable=False, server_default=sa.text('1')),

    )

    group_memberships.create()


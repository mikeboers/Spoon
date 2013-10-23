import sqlalchemy as sa


def upgrade(engine):

    meta = sa.MetaData(bind=engine)
    meta.reflect()

    existing = []

    if 'ssh_keys' in meta.tables:

        old = meta.tables['ssh_keys']
        for row in old.select().execute():
            existing.append((row.account_id, row.data))
        old.drop()

        meta = sa.MetaData(bind=engine)
        meta.reflect()

    new = sa.Table('ssh_keys', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id'), nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('data', sa.String, nullable=False),
        sa.Column('comment', sa.String, nullable=False),
    )
    new.create()

    for account_id, encoded in existing:
        type_, data, comment = encoded.split(None, 2)
        new.insert().execute(
            account_id=account_id,
            type=type_.strip(),
            data=data.strip(),
            comment=comment.strip(),
        )



import errno
import os
import re
import sys

from ..core.flask import app, db
from .account import Account


class SSHKey(db.Model):

    __tablename__ = 'ssh_keys'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )

    owner = db.relationship('Account', backref=db.backref('ssh_keys', cascade='save-update,delete,delete-orphan'))

    @property
    def clean(self):
        parts = self.data.strip().split()
        if parts[0] not in ('ssh-rsa', ):
            raise ValueError('unknown key format: %r' % parts[0])
        return '%s %s %s' % (parts[0], parts[1], self.owner.name)



_flags = ('# git-base start', '# git-base end')


def iter_authorized_keys():

    command_path = os.path.join(os.path.dirname(sys.executable), 'git-base-shell')
    format = 'command="%s %%s",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %%s' % command_path

    to_add = []
    for account in Account.query.all():
        for key in account.ssh_keys:
            try:
                yield format % (account.name, key.clean)
            except ValueError as e:
                print e


def rewrite_authorized_keys(path=None):

    if path is None:
        path = app.config['SSH_KEYS_PATH']

    try:
        content = open(path, 'r').read()
    except IOError:
        content = ''

    # re.sub doesn't work here?
    m = re.search(r'# git-base start.+git-base end', content, re.DOTALL)
    if m:
        content = content[:m.start()] + content[m.end():]
        content = content.rstrip()

    content = ''.join((
        content,
        '\n\n' if content else '',
        _flags[0],
        '\n',
        '\n'.join(iter_authorized_keys()),
        '\n',
        _flags[1],
        '\n',
    ))

    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with open(path, 'w') as fh:
        fh.write(content)


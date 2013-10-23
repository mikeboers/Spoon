import base64
import errno
import hashlib
import os
import re
import sys

from ..core import app, db
from .account import Account


class SSHKey(db.Model):

    __tablename__ = 'ssh_keys'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )

    owner = db.relationship('Account', backref=db.backref('ssh_keys', cascade='save-update,delete,delete-orphan'))

    def __init__(self, encoded=None, *args, **kwargs):
        if encoded is not None:

            m = re.match(r'^(ssh-rsa|ssh-dsa)\s+([a-zA-Z0-9+/]+=*)\s*(.+?)$', encoded, re.DOTALL)
            if not m:
                raise ValueError('badly formatted key')
            type_, data, comment = m.groups()

            conflicts = [k for k in ('type', 'data', 'comment') if k in kwargs]
            if conflicts:
                raise TypeError('got encoded and %s' % '/'.join(conflicts))

        else:
            try:
                type_ = kwargs.pop('type')
                data = kwargs.pop('data')
                comment = kwargs.pop('comment')
            except KeyError as e:
                raise TypeError('SSHKey requires %s' % e.args[0])

        if type_ not in ('ssh-rsa', 'ssh-dsa'):
            raise ValueError('unknown SSHKey type %r' % type_)
        try:
            roundtrip = base64.b64encode(base64.b64decode(data))
        except TypeError:
            roundtrip = None
        if data != roundtrip:
            raise ValueError('SSHKey data not base64')
        comment = comment.strip()

        super(SSHKey, self).__init__(type=type_, data=data, comment=comment, **kwargs)

    @property
    def fingerprint(self):
        digest = hashlib.md5(self.data.decode('base64')).hexdigest()
        return ':'.join(digest[i:i + 2] for i in xrange(0, len(digest), 2))

    @property
    def clean_comment(self):
        comment = re.sub(r'[^\w@\.-]+', '-', self.comment.strip())
        return comment

    def as_string(self):
        return '%s %s %s' % (self.type, self.data, self.clean_comment)



_flags = ('# spoon start', '# spoon end')


def iter_authorized_keys():

    vexec_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bin', 'vexec'))
    format = 'command="%s spoon-shell %%s",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %%s' % vexec_path

    to_add = []
    for account in Account.query.all():
        for key in account.ssh_keys:
            try:
                yield format % (account.name, key.as_string())
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
    m = re.search(r'# spoon start.+spoon end', content, re.DOTALL)
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


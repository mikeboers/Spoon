import os
import re

from .core.flask import app, db
from .models import User, SSHKey


_flags = ('# git-base start', '# git-base end')


def rewrite():

    try:
        content = open(app.config['SSH_KEYS_PATH'], 'r').read()
    except IOError:
        content = ''

    # re.sub doesn't work here?
    m = re.search(r'# git-base start.+git-base end', content, re.DOTALL)
    if m:
        content = content[:m.start()] + content[m.end():]

    command_path = os.path.join(app.root_path, 'bin', 'git-base-shell')
    format = 'command="%s %%s",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %%s' % command_path

    to_add = []
    for user in User.query.all():
        for key in user.ssh_keys:
            try:
                to_add.append(format % (user.login, key.cleaned))
            except ValueError as e:
                print e

    content = content.rstrip() + '\n\n' + _flags[0] + '\n' + '\n'.join(to_add) + '\n' + _flags[1] + '\n'
    with open(app.config['SSH_KEYS_PATH'], 'w') as fh:
        fh.write(content)


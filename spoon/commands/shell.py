#!/usr/bin/env python2.7

import getpass
import os
import re
import subprocess
import shlex
import sys

from flask.ext.login import login_user, current_user

from ..core import app, auth, db
from ..models import Account, Repo
from ..utils import *
from ..auth import dummy_anon


_commands = {}
def register(func):
    _commands[func.__name__] = func
    return func


@register
def echo(command, *args):
    print 'I got: %s' % ' '.join(args)


@register
def passwd(args, pass_=None):

    if pass_ is None:
        print 'Resetting password for "%s".' % current_user.name
        pass_ = getpass.getpass('New password: ')
        pass2 = getpass.getpass('Verify password: ')
        if pass_ != pass2:
            print 'Passwords do not match.'
            return 1

    current_user.set_password(pass_)
    db.session.commit()
    print 'Password updated.'


def main():
    

    if len(sys.argv) != 2:
        die('missing user')

    username = sys.argv[1]
    user = Account.query.filter_by(name=username).first()
    if not user:
        die('unknown user: %r' % username)

    # Log the user in. We need a fake request context to do it.
    app.test_request_context().push()
    login_user(user)

    args = shlex.split(os.environ.get('SSH_ORIGINAL_COMMAND', ''))

    if args[0] in ('git-upload-pack', 'git-receive-pack', 'git-upload-archive'):
        exit(do_git(*args))

    if args[0] in _commands:
        exit(_commands[args[0]](*args))

    die('unknown command: %r', args[0])


def do_git(command, *args):

    if len(args) != 1:
        die('expected one argument, got %r' % args)
    joined_name = args[0]

    m = re.match(r"^/?([^/]+)/(.+)(?:.git)?/?$", joined_name)
    if not m:
        die('bad command argument: %r', joined_name)

    account_name, repo_name = m.groups()

    # TODO: pass results of user.has_permission('repo.create')
    try:
        repo = Repo.lookup(account_name, repo_name, create=True)
    except (ValueError, RuntimeError) as e:
        die(str(e))

    # It doesn't exist, and we don't have permission to create it.
    if not repo:
        die('unknown repo %s/%s' % (account_name, repo_name))

    # Make sure we are allowed to operate on it. Same error as above.
    permission = 'repo.write' if command == 'git-receive-pack' else 'repo.read'
    if not auth.can(permission, repo):
        die('unknown repo %s/%s' % (account_name, repo_name))

    # Allow the call to go through.
    debug('calling %s %s/%s', command, account_name, repo_name)
    os.execvp(command, [command, repo.path])


import contextlib
import datetime
import errno
import functools
import logging
import os
from unittest import TestCase as BaseTestCase
from subprocess import call, check_output, CalledProcessError

import werkzeug as wz
from flask.ext.login import current_user, login_user

from spoon.core import app, auth, db
from spoon.auth import dummy_admin, dummy_anon
from spoon.models import Account, Repo, GroupMembership


def mini_uuid():
    return os.urandom(4).encode('hex')


def mini_timestamp():
    return datetime.datetime.now().strftime('%y%m%d%H%M%S')

mini_start = mini_timestamp()


def shell(source, key=None, __output__=False, **kwargs):
    if key:
        source = ('ssh-add "%s" 2>/dev/null\n' % key) + source
    return (check_output if __output__ else call)(['ssh-agent', 'bash', '-c', source], **kwargs)


shell_output = functools.partial(shell, __output__=True)


CLEAN_DB = os.environ.get('CLEAN_DB', '1')


sandbox = os.path.join(
    os.path.dirname(__file__),
    'sandbox',
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
)


def genkey(name):
    path = os.path.join(sandbox, name)
    if not os.path.exists(path):
        call(['ssh-keygen', '-q', '-t', 'rsa', '-b', '1024', '-P', '', '-f', path])
    return path


class TestCase(BaseTestCase):

    needs_context = False

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.context = None

    def setUp(self):
        if self.needs_context:
            self.context = app.test_request_context()
            self.context.push()

    def tearDown(self):
        if self.context is not None:
            self.context.pop()


    @classmethod
    def _sandbox(cls):
        path = os.path.join(sandbox, cls.__name__)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    @wz.utils.cached_property
    def sandbox(self):
        return self._sandbox()

    @classmethod
    def _log(cls):
        return logging.getLogger(cls.__module__ + '.' + cls.__name__)

    @wz.utils.cached_property
    def log(self):
        return self._log()

    @classmethod
    def genkey(cls, name='id_rsa'):
        return genkey(os.path.join(cls._sandbox(), name))


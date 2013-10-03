import contextlib
import datetime
import functools
import os
from unittest import TestCase as BaseTestCase
from subprocess import call, check_output, CalledProcessError

from flask.ext.login import current_user, login_user

from gitbase.core.flask import app, auth, db
from gitbase.auth import dummy_admin, dummy_anon
from gitbase.models import Account, Repo, GroupMembership


def mini_uuid():
    return os.urandom(4).encode('hex')


def mini_timestamp():
    return datetime.datetime.now().strftime('%y%m%d%H%M%S')


shell = functools.partial(call, shell=True)
shell_output = functools.partial(check_output, shell=True)


sandbox = os.path.join(
    os.path.dirname(__file__),
    'sandbox',
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
)


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

    @property
    def sandbox(self):
        path = os.path.join(sandbox, self.__class__.__name__)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path


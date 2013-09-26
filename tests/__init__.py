import datetime
import os
from unittest import TestCase as BaseTestCase

from flask.ext.login import current_user, login_user

from gitbase.core.flask import app, auth, db
from gitbase.auth import dummy_admin, dummy_anon
from gitbase.models import User, Group, Repo, Membership


sandbox = os.path.join(
    os.path.dirname(__file__),
    'sandbox',
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S'),
)


class TestCase(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.context = None

    def setUp(self):
        self.context = app.test_request_context()
        self.context.push()

    def tearDown(self):
        if self.context is not None:
            self.context.pop()

    @property
    def sandbox(self):
        path = os.path.join(sandbox, self.full_name)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path


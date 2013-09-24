import logging
import re

import sqlalchemy as sa
import werkzeug as wz

from ..utils import debug
from . import app, db


log = logging.getLogger(__name__)


class User(db.Model):

    __tablename__ = 'users'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    def is_authenticated(self):
        '''Returns True if the user is authenticated.

        i.e. they have provided valid credentials. (Only authenticated users
        will fulfill the criteria of login_required.)

        '''

        return True

    def is_active(self):
        '''Returns True if this is an active user.

        In addition to being authenticated, they also have activated their
        account, not been suspended, or any condition your application has for
        rejecting an account. Inactive accounts may not log in (without being
        forced of course).

        '''

        return True

    def is_anonymous(self):
        '''Returns True if this is an anonymous user.

        Actual users should return False instead.

        '''

        return False

    def get_id(self):
        '''Returns a unicode that uniquely identifies this user.

        Can be used to load the user from the user_loader callback. Note that
        this must be a unicode - if the ID is natively an int or some other
        type, you will need to convert it to unicode.

        '''

        return self.login

import os
import re
import shutil

import bcrypt
import sqlalchemy as sa
import werkzeug as wz
from flask.ext.login import current_user

from ..utils import debug
from ..core.flask import app, auth, db
from .groupmembership import GroupMembership
from .roleset import RoleSetColumn


class Account(db.Model):

    __tablename__ = 'accounts'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )
    
    roles = RoleSetColumn()

    def __repr__(self):
        return '<%s %s:%s>' % (
            self.__class__.__name__,
            'group' if self.is_group else 'user',
            self.name
        )

    @property
    def path(self):
        return os.path.join(app.config['REPO_DIR'], self.name)

    @classmethod
    def lookup(cls, name, create=False):

        # Make sure it is a valid name.
        if not re.match(app.config['ACCOUNT_NAME_RE'], name):
            raise ValueError('invalid account name: %r' % name)

        account = cls.query.filter_by(name=name).first()
        if not account:

            # Bail if it wasn't requested to create it.
            if not create:
                return

            # Bail if we don't have permission to create it.
            # TODO: make this check for can('account.create', current_user).
            if 'wheel' not in current_user.roles:
                return

            debug('creating group %s', name)
            account = Account(name=name, is_group=True)

            # Only create a membership if this is a real user.
            if current_user.id:
                account.members.append(GroupMembership(
                    user=current_user,
                    is_admin=True, # Should this be the case?
                ))

            db.session.add(account)
            db.session.commit()

        return account

    @property
    def __acl__(self):
        yield 'ALLOW ROOT ANY'

        # TODO: user specified goes here.

        yield 'ALLOW SELF repo.create'
        yield 'ALLOW SELF accoun.write'

        yield 'ALLOW ADMIN repo.create'
        yield 'ALLOW ADMIN account.write'
        yield 'ALLOW MEMBER account.read'

        if self.is_public:
            yield 'ALLOW ANY account.read'
        else:
            # Surpress the public's ability to do anything within this
            # account, without those objects needing to know about it.
            yield 'DENY !MEMBER ANY'


    @property
    def __acl_context__(self):
        return dict(
            account=self,
        )

    @wz.cached_property
    def readable_repos(self):
        return [r for r in self.repos if auth.can('repo.read', r)]

    def delete(self):
        shutil.rmtree(self.path, ignore_errors=True)
        db.session.delete(self)
        db.session.commit()


    # User stuff:

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return self.password_hash and bcrypt.checkpw(password, self.password_hash)

    def is_authenticated(self):
        """For Flask-Login."""
        return True

    def is_active(self):
        """For Flask-Login."""
        return True

    def is_anonymous(self):
        """For Flask-Login."""
        return False

    def get_id(self):
        """For Flask-Login."""
        return self.name


class AccountConverter(wz.routing.BaseConverter):

    def __init__(self, url_map):
        super(AccountConverter, self).__init__(url_map)
        self.regex = app.config['ACCOUNT_NAME_RE']

    def to_python(self, name):
        try:
            account = Account.lookup(name)
            if account:
                return account
        except ValueError:
            pass
        raise wz.routing.ValidationError('account does not exist: %r' % name)

    def to_url(self, account):
        return account.name


app.url_map.converters['account'] = AccountConverter


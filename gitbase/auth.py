import logging

from flask import request
from flask.ext.acl.predicates import string_predicates
from flask.ext.acl.permissions import string_permissions
from flask.ext.login import current_user, UserMixin, AnonymousUserMixin

from .core.flask import app, auth
from .models import Repo, Account

log = logging.getLogger(__name__)



@auth.context_processor
def provide_user():
    return dict(user=current_user)


@app.before_request
def assert_can_access_url_pieces():
    for v in (request.view_args or {}).itervalues():
        if isinstance(v, Repo):
            auth.assert_can('repo.read', v)
        if isinstance(v, Account):
            auth.assert_can('account.read', v)


class Role(object):

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)
    def __call__(self, user, **kw):
        return self.name in getattr(user, 'roles', ())


class ADMIN(object):

    def __repr__(self):
        return 'ADMIN'
    def __call__(self, user, account=None, **kw):
        # log.info('check if %r is an admin' % user)
        if not user.is_authenticated() or not account:
            return
        membership = next((m for m in account.members if m.user == user), None)
        return membership and membership.is_admin


class OWNER(object):

    def __repr__(self):
        return 'OWNER'
    def __call__(self, user, account=None, **kw):
        # log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
        return user.is_authenticated() and account and account == user


class MEMBER(object):

    def __repr__(self):
        return 'MEMBER'
    def __call__(self, user, account=None, **kw):
        # log.info('check if %r is member of %r' % (current_user, group))
        return (
            user.is_authenticated() and
            account and
            any(m.user == user for m in account.members)
        )


string_predicates['ROOT'] = Role('wheel')
string_predicates['OBSERVER'] = Role('observer')
string_predicates['OWNER'] = OWNER()
string_predicates['MEMBER'] = MEMBER()
string_predicates['ADMIN'] = ADMIN()

string_permissions['repo.delete'] = set(('repo.delete', 'repo.write', 'repo.read'))
string_permissions['repo.write'] = set(('repo.write', 'repo.read'))
string_permissions['account.write'] = set(('account.write', 'account.read'))

# TODO: remove this quick fix.
string_permissions['group.write'] = set(('account.write', 'account.read'))
string_permissions['group.read'] = set(('account.read', ))


class _DummyAdmin(UserMixin):

    id = 0
    is_group = False
    name = 'ADMIN'
    groups = []
    roles = set(('wheel', ))

    __repr__ = lambda self: '<DummyAccount user:ADMIN>'

dummy_admin = _DummyAdmin()


class _DummyAnonymous(UserMixin):

    id = 0
    is_group = False
    name = 'ANONYMOUS'
    groups = []
    roles = set()

    __repr__ = lambda self: '<DummyAccount user:ANONYMOUS>'

dummy_anon = _DummyAnonymous()



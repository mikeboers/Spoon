import logging

from flask import request
from flask.ext.acl.predicates import string_predicates
from flask.ext.acl.permissions import string_permissions
from flask.ext.login import current_user, UserMixin, AnonymousUserMixin

from .core.flask import app, auth
from .models import Repo, Group

log = logging.getLogger(__name__)



@auth.context_processor
def provide_user():
    return dict(user=current_user)


@app.before_request
def assert_can_access_url_pieces():
    for v in (request.view_args or {}).itervalues():
        if isinstance(v, Repo):
            auth.assert_can('repo.read', v)
        if isinstance(v, Group):
            auth.assert_can('group.read', v)


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
    def __call__(self, user, group, **kw):
        # log.info('check if %r is an admin' % user)
        if not user.is_authenticated() or not group:
            return
        membership = next((m for m in group.memberships if m.user == user), None)
        return membership and membership.is_admin


class OWNER(object):

    def __repr__(self):
        return 'OWNER'
    def __call__(self, user, group=None, **kw):
        # log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
        return user.is_authenticated() and group and group.owner == user


class MEMBER(object):

    def __repr__(self):
        return 'MEMBER'
    def __call__(self, user, group=None, **kw):
        # log.info('check if %r is member of %r' % (current_user, group))
        return (
            user.is_authenticated() and
            group and
            any(m.user == user for m in group.memberships)
        )


string_predicates['ROOT'] = Role('wheel')
string_predicates['OBSERVER'] = Role('observer')
string_predicates['OWNER'] = OWNER()
string_predicates['MEMBER'] = MEMBER()
string_predicates['ADMIN'] = ADMIN()

string_permissions['repo.delete'] = set(('repo.delete', 'repo.write', 'repo.read'))
string_permissions['repo.write'] = set(('repo.write', 'repo.read'))
string_permissions['group.write'] = set(('group.write', 'group.read'))


dummy_admin = UserMixin()
dummy_admin.id = 0
dummy_admin.name='<ADMIN>'
dummy_admin.is_admin = True
dummy_admin.home = None
dummy_admin.memberships = []

dummy_anon = AnonymousUserMixin()
dummy_anon.name='<ANON>'
dummy_anon.id = 0
dummy_anon.is_admin = False
dummy_anon.home = None
dummy_anon.memberships = []


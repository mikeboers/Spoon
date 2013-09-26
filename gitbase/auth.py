import logging

from flask import request
from flask.ext.acl.predicates import string_predicates
from flask.ext.login import current_user, UserMixin, AnonymousUserMixin

from .core.flask import app, auth
from .models import Repo, Group

log = logging.getLogger(__name__)



@auth.context_processor
def provide_user():
    return dict(current_user=current_user)


@app.before_request
def assert_can_access_url_pieces():
    for v in request.view_args.itervalues():
        if isinstance(v, Repo):
            auth.assert_can('repo.read', v)
        if isinstance(v, Group):
            auth.assert_can('group.read', v)


class ADMIN(object):

    def __repr__(self):
        return 'ADMIN'
    def __call__(self, current_user, **kw):
        # log.info('check if %r is an admin' % current_user)
        return current_user.is_authenticated() and current_user.is_admin


class OWNER(object):

    def __repr__(self):
        return 'OWNER'
    def __call__(self, current_user, group=None, **kw):
        # log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
        return current_user.is_authenticated() and group and group.owner == current_user


class MEMBER(object):

    def __repr__(self):
        return 'MEMBER'
    def __call__(self, current_user, group=None, **kw):
        # log.info('check if %r is member of %r' % (current_user, group))
        return (
            current_user.is_authenticated() and
            group and
            any(m.current_user == current_user for m in group.memberships)
        )


string_predicates['OWNER'] = OWNER()
string_predicates['MEMBER'] = MEMBER()
string_predicates['ADMIN'] = ADMIN()


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


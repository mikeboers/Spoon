import logging

from flask import request
from flask.ext.acl.predicates import string_predicates
from flask.ext.login import current_user, UserMixin

from .core.flask import app, auth
from .models import Repo, Group

log = logging.getLogger(__name__)


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
    def __call__(self, **kw):
        # log.info('check if %r is an admin' % current_user)
        return current_user.is_authenticated() and current_user.is_admin

class OWNER(object):

    def __repr__(self):
        return 'OWNER'
    def __call__(self, group=None, **kw):
        # log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
        return current_user.is_authenticated() and group and group.owner == current_user

class MEMBER(object):

    def __repr__(self):
        return 'MEMBER'
    def __call__(self, group=None, **kw):
        # log.info('check if %r is member of %r' % (current_user, group))
        return (
            current_user.is_authenticated() and
            group and
            any(m.user == current_user for m in group.memberships)
        )


string_predicates['OWNER'] = OWNER()
string_predicates['MEMBER'] = MEMBER()
string_predicates['ADMIN'] = ADMIN()


dummy_admin = UserMixin()
dummy_admin.id = 0
dummy_admin.is_admin = True
dummy_admin.home = None
dummy_admin.memberships = []

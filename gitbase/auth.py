import logging

from flask import request
from flask.ext.acl.predicates import string_predicates
from flask.ext.login import current_user

from .main import app, auth
from .models import Repo, Group

log = logging.getLogger(__name__)


@app.before_request
def assert_can_access_url_pieces():
    for v in request.view_args.itervalues():
        if isinstance(v, (Repo, Group)):
            auth.assert_can('read', v)


def check_admin(**kw):
    # log.info('check if %r is an admin' % current_user)
    return current_user.is_authenticated() and current_user.is_admin


def check_owner(repo=None, group=None, **kw):
    # log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
    return current_user.is_authenticated() and repo.owner == current_user


def check_members(group=None, **kw):
    # log.info('check if %r is member of %r' % (current_user, group))
    return current_user.is_authenticated() and current_user in group.members


string_predicates['OWNER'] = check_owner
string_predicates['MEMBER'] = check_members
string_predicates['ADMIN'] = check_admin

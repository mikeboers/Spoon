import logging

from flask.ext.acl.predicates import string_predicates
from flask.ext.login import current_user


log = logging.getLogger(__name__)



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

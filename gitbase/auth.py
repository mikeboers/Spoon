import logging

from flask.ext.acl.predicates import string_predicates
from flask.ext.login import current_user


log = logging.getLogger(__name__)


def check_owner(repo=None, group=None, **kw):
    log.info('check if %r is owner of %r/%r' % (current_user, group, repo))
    return True


def check_members(group=None, **kw):
    log.info('check if %r is member of %r' % (current_user, group))
    return True


string_predicates['OWNER'] = check_owner
string_predicates['MEMBERS'] = check_members

from __future__ import absolute_import

import sqlalchemy as sa
from flask import request, abort, flash, redirect, url_for
from flask.ext.login import current_user

from ..core.flask import app, db, auth
from ..core.mako import render_template

from ..models import Group, Repo, User, GroupMembership


requires_root = lambda func: auth.ACL('''
    ALLOW ROOT ANY
    DENY ALL ANY
''')(func)


# --- Register the pages.

from . import login
from . import index
from . import group
from . import repo
from . import tree
from . import commit
from . import user

from . import debug
from . import cpanel
from . import clone

from . import api

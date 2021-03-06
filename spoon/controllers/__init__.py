from __future__ import absolute_import

import sqlalchemy as sa
from flask import request, abort, flash, redirect, url_for
from flask.ext.login import current_user
from flask.ext.roots.mako import render_template

from ..core import app, db, auth

from ..models import Account, Repo, GroupMembership


requires_root = lambda func: auth.ACL('''
    ALLOW ROOT ANY
    DENY ALL ANY
''')(func)


# --- Register the pages.

from . import login
from . import index
from . import account
from . import repo
from . import tree
from . import commit

from . import debug
from . import cpanel
from . import clone

from . import api

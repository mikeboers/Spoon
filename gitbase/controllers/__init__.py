from __future__ import absolute_import

from flask import request

from ..core.flask import app, db
from ..core.mako import render_template


# --- Register the pages.

from . import index

from flask.ext.roots import make_app

app = make_app(__name__)

db = app.roots.db
mako = app.roots.mako
login_manager = app.roots.login_manager
auth = app.roots.auth

# Register other components.
from . import auth as _auth
from . import models

# Controllers are NOT registered here!

from gitbase.core.flask import app, auth, db


# Register things.
from gitbase import auth as _auth
from gitbase import models
from gitbase import controllers


db.create_all()

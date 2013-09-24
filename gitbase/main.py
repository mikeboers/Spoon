from gitbase.core.flask import app, db


# Register things.
from gitbase import auth
from gitbase import models
from gitbase import controllers


db.create_all()

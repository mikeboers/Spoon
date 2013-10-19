from spoon.core import app, auth, db


# Register things.
from spoon import auth as _auth
from spoon import models
from spoon import controllers


db.create_all()

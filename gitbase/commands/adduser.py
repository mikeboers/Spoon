import sys

from ..core.flask import app, db
from ..models import User


def main():

    user = User(login=sys.argv[1])
    db.session.add(user)
    db.session.commit()

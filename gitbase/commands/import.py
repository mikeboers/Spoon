import os

from flask.ext.login import login_user

from ..core.flask import app
from ..models import Repo
from ..auth import dummy_admin
from ..utils import stderr


def main():

    # We need a fake request context to do this.
    app.test_request_context().push()
    login_user(dummy_admin)

    for group_name in os.listdir(app.config['REPO_DIR']):
        for repo_name in os.listdir(os.path.join(app.config['REPO_DIR'], group_name)):

            repo_name, ext = os.path.splitext(repo_name)
            if ext != '.git':
                continue

            try:
                repo = Repo.lookup(group_name, repo_name, create=True)
            except ValueError as e:
                stderr(e)




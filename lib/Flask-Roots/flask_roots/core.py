from __future__ import absolute_import

import os

from flask import Flask as Base
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.imgsizer import ImgSizer
# from flask.ext.mail import Mail
from flask.helpers import send_from_directory
from flask.ext.login import LoginManager
from flask.ext.acl import AuthManager


class Flask(Base):

    def send_static_file(self, filename):

        # Ensure get_send_file_max_age is called in all cases.
        # Here, we ensure get_send_file_max_age is called for Blueprints.
        cache_timeout = self.get_send_file_max_age(filename)

        # Serve out of 'static' and 'var/static'.
        for dir_name in 'static', 'var/static':
            dir_path = os.path.join(self.root_path, dir_name)
            file_path = os.path.join(dir_path, filename)
            if os.path.exists(file_path):
                break
        
        return send_from_directory(dir_path, filename,
                                   cache_timeout=cache_timeout)


def make_app(*args, **kwargs):

    kwargs.setdefault('static_url_path', '')
    app = Flask(*args, **kwargs)

    from .config import make_config
    app.config.update(make_config(app))

    app.root_path = app.config['ROOT_PATH']

    from .logs import setup_logs
    setup_logs(app)

    from .session import setup_session
    setup_session(app)

    login_manager = LoginManager(app)
    auth = AuthManager(app)

    from .mako import MakoTemplates
    mako = MakoTemplates(app)

    imgsizer = ImgSizer(app)

    db = SQLAlchemy(app)
    db.metadata.bind = db.engine # WTF do I need to do this for?!

    from .routing import setup_routing
    setup_routing(app)

    from .errors import setup_errors
    setup_errors(app)

    return dict(
        app=app,
        mako=mako,
        auth=auth,
        login_manager=login_manager,
        imgsizer=imgsizer,
        db=db,
    )


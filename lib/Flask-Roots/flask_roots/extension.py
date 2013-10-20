from __future__ import absolute_import

import os

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.imgsizer import ImgSizer
# from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.acl import AuthManager


class Roots(object):

    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):

        # Link them together.
        self.app = app
        app.roots = self
        app.extensions['roots'] = self

        from .config import make_config
        app.config.update(make_config(app.name))
        app.root_path = app.config['ROOT_PATH']
        app.instance_path = app.config['INSTANCE_PATH']

        from .logs import setup_logs
        setup_logs(app)

        from .session import setup_session
        setup_session(app)

        self.login_manager = LoginManager(app)
        self.auth = AuthManager(app)

        from .mako import MakoTemplates
        self.mako = MakoTemplates(app)

        self.imgsizer = ImgSizer(app)

        self.db = SQLAlchemy(app)
        self.db.metadata.bind = self.db.engine # WTF do I need to do this for?!

        from .routing import setup_routing
        setup_routing(app)

        from .errors import setup_errors
        setup_errors(app)


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


app = Flask(__name__,

    # Expose everything in the static folder at the URL root.
    static_url_path='',

)

app.config.from_object('gitbase.core.config')
app.root_path = app.config['ROOT_PATH']


# Setup logging before any extensions. Must be imported *after* the app is
# configured so that logging can use that configuration.
from . import logs

# Extensions that must be imported after app.core.app exists.
from .mako import MakoTemplates


imgsizer = ImgSizer(app)
mako = MakoTemplates(app)
db = SQLAlchemy(app)
# mail = Mail(app)
login_manager = LoginManager(app)
auth = AuthManager(app)

# WTF do I need to do this for?!
db.metadata.bind = db.engine


# Setup routing extensions (regexes).
# from . import routing


# Setup error handlers.
from . import errors


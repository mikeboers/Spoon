from flask.ext.roots import make_app

globals().update(make_app(__name__))

from .flask import Flask
from .extension import Roots

def make_app(*args, **kwargs):
    app = Flask(*args, **kwargs)
    Roots(app)
    return app


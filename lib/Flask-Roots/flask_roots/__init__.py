from .flask import Flask
from .extension import Roots

def make_app(*args, **kwargs):
    app = Flask(*args, **kwargs)
    roots = Roots(app)
    return roots.export()


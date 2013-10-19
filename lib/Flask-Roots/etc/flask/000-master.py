import os

UPLOAD_FOLDER = os.path.join(INSTANCE_PATH, 'uploads')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_PATH, 'sqlite', 'main.sqlite')

# This will get overriden in a subsequent configfile, but we want something
# completly random in here just in case.
SECRET_KEY = os.urandom(32)

setdefault('MAKO_IMPORTS', []).append('from flask.ext.imgsizer import resized_img_src')
MAKO_MODULE_DIRECTORY = os.path.join(INSTANCE_PATH, 'mako')

setdefault('IMGSIZER_PATH', [])
IMGSIZER_PATH.extend(
    os.path.join(root, name)
    for name in ('assets', 'static')
    for root in (INSTANCE_PATH, ROOT_PATH)
)

IMGSIZER_CACHE = os.path.join(INSTANCE_PATH, 'imgsizer')

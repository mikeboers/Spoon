import os

UPLOAD_FOLDER = os.path.join(INSTANCE_PATH, 'uploads')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_PATH, 'sqlite', 'main.sqlite')

# Create a persistant secret key.
secret_key_path = os.path.join(INSTANCE_PATH, 'etc', 'secret_key')
if not os.path.exists(secret_key_path):
    with open(secret_key_path, 'w') as fh:
        fh.write(os.urandom(32))
with open(secret_key_path) as fh:
    SECRET_KEY = fh.read()


# TODO: migrate this to Flask-Imgsizer
setdefault('MAKO_IMPORTS', []).append('from flask.ext.imgsizer import resized_img_src')

MAKO_MODULE_DIRECTORY = os.path.join(INSTANCE_PATH, 'mako')

setdefault('IMGSIZER_PATH', [])
IMGSIZER_PATH.extend(
    os.path.join(root, name)
    for name in ('assets', 'static')
    for root in (INSTANCE_PATH, ROOT_PATH)
)

IMGSIZER_CACHE = os.path.join(INSTANCE_PATH, 'imgsizer')

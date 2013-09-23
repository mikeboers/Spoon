import os


DOMAIN = 'mikeboers.com'
PORT = 8000

UPLOAD_FOLDER = os.path.join(ROOT_PATH, 'var', 'uploads')


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ROOT_PATH, 'var', 'sqlite', 'main.sqlite')

# This will get overriden in a subsequent configfile, but we want something
# completly random in here just in case.
SECRET_KEY = os.urandom(32)

# MAKO_IMPORTS = ['from flask.ext.imgsizer import resized_img_src, resized_img_src as auto_img_src']
MAKO_MODULE_DIRECTORY = os.path.join(ROOT_PATH, 'var', 'mako')

IMGSIZER_PATH = [os.path.join(ROOT_PATH, x) for x in (
    'var/assets', 'var/static', 'assets', 'static',
)]
IMGSIZER_CACHE = os.path.join(ROOT_PATH, 'var', 'imgsizer')

ADMINS = ['admin@mikeboers.com']

# Just for now, until I get everything stablized again.
CSRF_ENABLED = False


FLICKR_NSID = '24585471@N05'

BLOG_POSTS_PER_PAGE = 10

AKISMET_API_KEY = 'cac47c4f9bf3'
AKISMET_DOMAIN = 'http://mikeboers.com'

DEFAULT_MAIL_SENDER = 'website@mikeboers.com'

FLICKR_API_KEYS = ('secret', 'public')
MASTER_PASSWORD = None

TWITTER_SCREEN_NAME = 'mikeboers'



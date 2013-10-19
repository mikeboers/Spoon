import os

DOMAIN = 'git.mikeboers.com'
PORT = 8000

ADMINS = ['admin@mikeboers.com']
DEFAULT_MAIL_SENDER = 'website@mikeboers.com'

REPO_DIR = os.path.join(INSTANCE_PATH, 'repositories')

ACCOUNT_NAME_RE = r'[\w\.-]+'
REPO_NAME_RE  = r'[\w\.-]+'

SSH_KEYS_PATH = os.path.join(INSTANCE_PATH, 'ssh', 'authorized_keys')

COMMITS_PER_PAGE = 50

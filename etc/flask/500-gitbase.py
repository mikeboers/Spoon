import os

REPO_DIR = os.path.join(ROOT_PATH, 'var', 'repositories')

ACCOUNT_NAME_RE = r'[\w\.-]+'
REPO_NAME_RE  = r'[\w\.-]+'

SSH_KEYS_PATH = os.path.join(ROOT_PATH, 'var', 'ssh', 'authorized_keys')

COMMITS_PER_PAGE = 50

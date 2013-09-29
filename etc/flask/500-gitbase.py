import os

REPO_DIR = os.path.join(ROOT_PATH, 'var', 'repositories')

GROUP_NAME_RE = r'[\w\.-]+'
REPO_NAME_RE  = r'[\w\.-]+'

SSH_KEYS_PATH = os.path.join(ROOT_PATH, 'var', 'authorized_keys')

COMMITS_PER_PAGE = 50

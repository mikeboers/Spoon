#!/usr/bin/env python2.7

import os
import re
import subprocess
import sys

from ..main import app, db
from ..models import Group, Repo
from ..utils import *


def main():
        
    command = os.environ.get('SSH_ORIGINAL_COMMAND', '')
    command_parts = command.split(None, 1)
    if len(command_parts) != 2:
        die('bad command format: %r', command)

    git_command, raw_repo_path = command_parts

    if git_command not in ('git-upload-pack', 'git-receive-pack', 'git-upload-archive'):
        die('bad command: %r', command)

    m = re.match(r"^'/?([^/]+)/(.+)(?:.git)?/?'$", raw_repo_path)
    if not m:
        die('bad command argument: %r', raw_repo_path[1:-1])

    group_name, repo_name = m.groups()

    # TODO: pass results of user.has_permission('repo.create')
    repo = Repo.lookup(group_name, repo_name, create=True)

    # Allow the call to go through.
    debug('calling %s %s/%s', git_command, group_name, repo_name)
    os.execvp(git_command, [git_command, repo.path])


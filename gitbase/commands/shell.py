#!/usr/bin/env python2.7

import os
import re
import subprocess
import sys

from ..main import app, db
from ..models import Group, Repo
from .utils import *


def main():
        
    command = os.environ.get('SSH_ORIGINAL_COMMAND', '')
    command_parts = command.split(None, 1)
    if len(command_parts) != 2:
        die('bad command format: %r', command)

    git_command, raw_repo_path = command_parts

    if git_command not in ('git-upload-pack', 'git-receive-pack', 'git-upload-archive'):
        die('bad command: %r', command)

    m = re.match(r"^'/?(%s)/(%s)(?:.git)?'$" % (app.config['GROUP_PATTERN'], app.config['REPO_PATTERN']), raw_repo_path)
    if not m:
        die('invalid repository name: %r', raw_repo_path[1:-1])

    group_name, repo_name = m.groups()


    group = Group.query.filter(Group.name == group_name).first()
    group_dir = os.path.join(app.config['REPO_DIR'], group_name)
    if not group:

        # TODO: make sure they have permission to create groups.
        debug('creating new group')
        makedirs(group_name)
        group = Group(name=group_name)
        db.session.add(group)
        db.session.commit()

    # TODO: make sure they have permission to create repos.
    # TODO: add our `update` hook for access control.
    repo_dir = os.path.join(group_dir, repo_name + '.git')
    if not os.path.exists(repo_dir):
        debug('creating new repository')
        makedirs(repo_dir)
        proc = subprocess.Popen(['git', 'init', '--bare', repo_dir], stdout=subprocess.PIPE)
        for line in proc.stdout:
            sys.stderr.write(line.replace(app.config['REPO_DIR'], ''))
        code = proc.wait()
        if code:
            die(code)

    repo = Repo.query.filter_by(group=group, name=repo_name).first()
    if not repo:     
        
        # Add it to the database.
        repo = Repo(name=repo_name, group=group)
        db.session.add(repo)
        db.session.commit()

    # Allow the call to go through.
    debug('calling %s %s/%s', git_command, group_name, repo_name)
    os.execvp(git_command, [git_command, repo_dir])


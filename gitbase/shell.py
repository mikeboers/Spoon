#!/usr/bin/env python2.7

import os
import re
import subprocess
import sys


# TODO: pull this from Flask.
config = {
    'REPO_DIR': os.path.abspath(os.path.join(__file__, '..', '..', 'var', 'repositories'))
}


def die(message, *args):
    code = 1
    if isinstance(message, int):
        code = message
        message = 'exited with code %s' % code
    elif args:
        message = message % args
    error(message)
    exit(code)


def stderr(*args):
    sys.stderr.write('%s\n' % ' '.join(str(x) for x in args))


def error(msg, *args):
    if args:
        msg = msg % args
    stderr('git-base-ssh:', msg)

debug = error


def main():
        
    command = os.environ.get('SSH_ORIGINAL_COMMAND', '')
    command_parts = command.split(None, 1)
    if len(command_parts) != 2:
        die('bad command format: %r', command)

    git_command, raw_repo_path = command_parts

    if git_command not in ('git-upload-pack', 'git-receive-pack', 'git-upload-archive'):
        die('bad command: %r', command)

    m = re.match(r"^'/?([\w\.-]+)/([\w\.-]+)(?:.git)?'$", raw_repo_path)
    if not m:
        die('invalid repository name: %r', raw_repo_path[1:-1])

    group_name, repo_name = m.groups()


    group_dir = os.path.join(config['REPO_DIR'], group_name)
    if not os.path.exists(group_dir):

        # TODO: make sure they have permission to create groups.
        # TODO: create this group in the database.
        debug('creating new group')
        os.makedirs(group_dir)

    repo_dir = os.path.join(group_dir, repo_name + '.git')
    if not os.path.exists(repo_dir):

        # TODO: make sure they have permission to create repos.
        # TODO: create this repo in the database.
        # TODO: add our `update` hook for access control.
        debug('creating new repository')
        proc = subprocess.Popen(['git', 'init', '--bare', repo_dir], stdout=subprocess.PIPE)
        for line in proc.stdout:
            sys.stderr.write(line.replace(config['REPO_DIR'], ''))
        code = proc.wait()
        if code:
            die(code)


    # Allow the call to go through.
    debug('calling %s %s/%s', git_command, group_name, repo_name)
    os.execvp(git_command, [git_command, repo_dir])


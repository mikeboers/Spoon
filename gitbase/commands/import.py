#!/usr/bin/env python2.7

import os
import re
import subprocess
import sys

from ..main import app, db
from ..models import Group, Repo

from .utils import *


def main():

    for group_name in os.listdir(app.config['REPO_DIR']):

        if not re.match(app.config['GROUP_PATTERN'], group_name):
            continue

        for repo_name in os.listdir(os.path.join(app.config['REPO_DIR'], group_name)):

            repo_name, ext = os.path.splitext(repo_name)

            if ext != '.git':
                continue
            if not re.match(app.config['REPO_PATTERN'], repo_name):
                continue

            group = Group.query.filter(Group.name == group_name).first()
            if not group:
                print 'Creating group', group_name
                group = Group(name=group_name)
                db.session.add(group)

            repo = Repo.query.filter(Repo.group == group).filter(Repo.name == repo_name).first()
            if not repo:
                print 'Creating repo', repo_name
                repo = Repo(name=repo_name, group=group)
                db.session.add(repo)

    db.session.commit()




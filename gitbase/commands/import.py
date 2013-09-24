#!/usr/bin/env python2.7

import os
import re
import subprocess
import sys

from ..main import app, db
from ..models import Group, Repo
from ..utils import *


def main():

    for group_name in os.listdir(app.config['REPO_DIR']):
        for repo_name in os.listdir(os.path.join(app.config['REPO_DIR'], group_name)):

            repo_name, ext = os.path.splitext(repo_name)
            if ext != '.git':
                continue

            try:
                repo = Repo.lookup(group_name, repo_name, create=True)
            except ValueError as e:
                stderr(e)




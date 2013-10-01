import logging
import os
import re
import shutil
import subprocess
import sys

import pygit2
import sqlalchemy as sa
import werkzeug as wz

from flask.ext.login import current_user

from ..utils import debug, makedirs
from ..core.flask import app, auth, db
from .group import Group


log = logging.getLogger(__name__)


class Repo(db.Model):

    __tablename__ = 'repos'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    group = db.relationship(Group, backref='repos')
    
    @property
    def __acl__(self):
        
        yield 'ALLOW ROOT ALL'
        yield 'ALLOW ADMIN ALL'
        yield 'ALLOW OWNER ALL'

        yield 'ALLOW ADMIN repo.delete'
        yield 'ALLOW MEMBER repo.write' # read is implied

        # TODO: user specified goes here.

        for ace in self.group.__acl__:
            yield ace

        if self.is_public:
            yield 'ALLOW ANY repo.read'
        else:
            yield 'DENY ANONYMOUS ANY'
        

    @property
    def __acl_context__(self):
        return dict(
            repo=self,
            group=self.group,
        )

    @property
    def git(self):
        return pygit2.Repository(self.path)

    @property
    def path(self):
        return os.path.join(app.config['REPO_DIR'], self.group.name, self.name + '.git')


    _display_name = db.Column('display_name', db.String)

    @property
    def display_name(self):
        return self._display_name or self.name

    @display_name.setter
    def display_name(self, v):
        self._display_name = v


    @classmethod
    def lookup(cls, group_name, repo_name, create=False):

        # Make sure it is a valid name.
        if not re.match(r'^%s$' % app.config['REPO_NAME_RE'], repo_name):
            raise ValueError('invalid repo name: %r' % repo_name)

        # Grab/create the group.
        group = Group.lookup(group_name, create=create)
        if not group:
            return

        did_create = False

        repo = Repo.query.filter_by(name=repo_name, group=group).first()
        repo_dir = os.path.join(app.config['REPO_DIR'], group_name, repo_name + '.git')
        repo_dir_exists = os.path.exists(repo_dir)

        if not repo and repo_dir_exists:
            raise RuntimeError('repo already exists on disk; delete first')
        if repo and not repo_dir_exists:
            raise RuntimeError('repo does not exist on disk; create first')

        if not repo:

            # Make sure there are permissions.
            if not (create and auth.can('repo.create', group)):
                return

            debug('creating repository %s/%s', group_name, repo_name)
            makedirs(repo_dir)
            proc = subprocess.Popen(['git', 'init', '--bare', repo_dir], stdout=subprocess.PIPE)
            for line in proc.stdout:
                sys.stderr.write(line.replace(app.config['REPO_DIR'], ''))
            code = proc.wait()
            if code:
                shutil.rmtree(repo_dir, ignore_errors=True)
                raise RuntimeError('repo creation failed with code %d' % code)

            repo = Repo(name=repo_name, group=group)
            db.session.add(repo)
            db.session.commit()

        return repo

    def delete(self):
        shutil.rmtree(self.path, ignore_errors=True)
        db.session.delete(self)
        db.session.commit()



class RepoConverter(wz.routing.BaseConverter):

    def __init__(self, url_map):
        super(RepoConverter, self).__init__(url_map)
        self.regex = app.config['GROUP_NAME_RE'] + '/' + app.config['REPO_NAME_RE']

    def to_python(self, value):
        group_name, repo_name = value.split('/', 1)

        try:
            repo = Repo.lookup(group_name, repo_name)
            if repo:
                return repo
        except ValueError:
            pass
        raise wz.routing.ValidationError('repo does not exist: %r' % value)

    def to_url(self, repo):
        return '%s/%s' % (repo.group.name, repo.name)


app.url_map.converters['repo'] = RepoConverter


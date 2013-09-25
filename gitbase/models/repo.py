import logging
import os
import re
import subprocess
import sys

import pygit2
import sqlalchemy as sa
import werkzeug as wz

from ..utils import debug, makedirs

from . import app, db, Group


log = logging.getLogger(__name__)


class Repo(db.Model):

    __tablename__ = 'repos'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    group = db.relationship(Group, backref='repos')
    owner = db.relationship('User', backref='repos')
    
    @property
    def __acl__(self):
        yield 'ALLOW ADMIN ALL'
        yield 'ALLOW OWNER ALL'
        # TODO: user specified goes here.
        for ace in self.group.__acl__:
            yield ace
        if self.is_public:
            yield 'ALLOW ANY read'

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

    @classmethod
    def lookup(cls, group_name, repo_name, create=False):

        if not re.match(r'^%s$' % app.config['REPO_NAME_RE'], repo_name):
            raise ValueError('invalid repo name: %r' % repo_name)

        group = Group.lookup(group_name, create=create)
        if not group:
            return

        repo_dir = os.path.join(app.config['REPO_DIR'], group_name, repo_name + '.git')
        if not os.path.exists(repo_dir):

            if not create:
                return

            # TODO: make sure they are allowed to do this.
            debug('creating bare repository %s/%s', group_name, repo_name)
            makedirs(repo_dir)
            proc = subprocess.Popen(['git', 'init', '--bare', repo_dir], stdout=subprocess.PIPE)
            for line in proc.stdout:
                sys.stderr.write(line.replace(app.config['REPO_DIR'], ''))
            code = proc.wait()
            if code:
                raise RuntimeError('repo creation failed with code %d' % code)

        # No need to do a create permission check here, since we already did
        # that above.
        repo = Repo.query.filter_by(name=repo_name, group=group).first()
        if not repo:
            debug('importing repository %s/%s', group_name, repo_name)
            repo = Repo(name=repo_name, group=group)
            db.session.add(repo)
            db.session.commit()

        return repo



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


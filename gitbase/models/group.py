import logging
import re

import sqlalchemy as sa
import werkzeug as wz

from ..utils import debug
from . import app, db


log = logging.getLogger(__name__)


group_memberships_table = db.Table('group_memberships', db.metadata, autoload=True)


class Group(db.Model):

    __tablename__ = 'groups'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    members = db.relationship('User', secondary=group_memberships_table, backref='groups')

    @classmethod
    def lookup(cls, name, create=False):

        if not re.match(app.config['GROUP_NAME_RE'], name):
            raise ValueError('invalid group name: %r' % name)

        group = Group.query.filter_by(name=name).first()

        if not group:

            if not create:
                return

            # TODO: make sure they are allowed to do this.
            debug('importing group %s', name)
            group = Group(name=name)
            db.session.add(group)
            db.session.commit()

        return group


class GroupConverter(wz.routing.BaseConverter):

    def __init__(self, url_map):
        super(GroupConverter, self).__init__(url_map)
        self.regex = app.config['GROUP_NAME_RE']

    def to_python(self, name):
        try:
            group = Group.lookup(name)
            if group:
                return group
        except ValueError:
            pass
        raise wz.routing.ValidationError('group does not exist: %r' % name)

    def to_url(self, group):
        return group.name


app.url_map.converters['group'] = GroupConverter
import logging
import re

import sqlalchemy as sa
import werkzeug as wz

from ..utils import debug
from . import app, db


log = logging.getLogger(__name__)


class Group(db.Model):

    __tablename__ = 'groups'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    @classmethod
    def lookup(cls, name, create=False):

        name = name.lower()
        if not re.match(app.config['GROUP_NAME_RE'], name):
            raise ValueError('bad group name: %r' % name)

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
        raise ValidationError('group does not exist: %r' % name)

    def to_url(self, group):
        return group.name


app.url_map.converters['group'] = GroupConverter
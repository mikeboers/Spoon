import re

import sqlalchemy as sa
import werkzeug as wz
from flask.ext.login import current_user

from ..utils import debug
from ..core.flask import app, auth, db


class Group(db.Model):

    __tablename__ = 'groups'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    @property
    def is_a_home(self):
        return self.owner is not None
    
    @classmethod
    def lookup(cls, name, create=False):

        # Make sure it is a valid name.
        if not re.match(app.config['GROUP_NAME_RE'], name):
            raise ValueError('invalid group name: %r' % name)

        group = Group.query.filter_by(name=name).first()
        if not group:

            # Bail if it wasn't requested to create it.
            if not create:
                return

            # Bail if we don't have permission to create it.
            # TODO: make this check for can('group.create', current_user).
            if not current_user.is_admin:
                return

            debug('creating group %s', name)
            group = Group(name=name)

            # Only create a membership if this is a real user.
            if current_user.id:
                group.memberships.append(Membership(
                    user=current_user,
                    ))

            db.session.add(group)
            db.session.commit()

        return group

    @property
    def __acl__(self):
        yield 'ALLOW ROOT ANY'

        # TODO: user specified goes here.

        yield 'ALLOW ADMIN repo.create'
        yield 'ALLOW ADMIN group.write'
        yield 'ALLOW MEMBER group.read'

        if self.is_public:
            yield 'ALLOW ANY group.read'
        else:
            # Surpress the public's ability to do anything within this
            # group, without those objects needing to know about it.
            yield 'DENY !MEMBER ANY'


    @property
    def __acl_context__(self):
        return dict(
            group=self,
        )

    @wz.cached_property
    def readable_repos(self):
        return [r for r in self.repos if auth.can('repo.read', r)]


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


# Circular imports
from .membership import Membership

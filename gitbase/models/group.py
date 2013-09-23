import logging

import sqlalchemy as sa
import werkzeug as wz

from . import app, db


log = logging.getLogger(__name__)


class Group(db.Model):

    __tablename__ = 'groups'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

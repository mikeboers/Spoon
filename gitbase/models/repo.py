import logging

import sqlalchemy as sa
import werkzeug as wz

from . import app, db


log = logging.getLogger(__name__)


class Repo(db.Model):

    __tablename__ = 'repos'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    group = db.relationship('Group', backref='repos')


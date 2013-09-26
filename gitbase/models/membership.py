import sqlalchemy as sa

from ..core.flask import db


class Membership(db.Model):

    __tablename__ = 'memberships'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )

    user = db.relationship('User', backref=db.backref('memberships', cascade="all, delete-orphan"))
    group = db.relationship('Group', backref=db.backref('memberships', cascade="all, delete-orphan"))


import sqlalchemy as sa

from ..core.flask import db


class GroupMembership(db.Model):

    __tablename__ = 'group_memberships'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )

    user = db.relationship('Account',
        foreign_keys='GroupMembership.user_id',
        backref=db.backref('groups', cascade="all, delete-orphan"),
    )
    
    group = db.relationship('Account',
        foreign_keys='GroupMembership.group_id',
        backref=db.backref('members', cascade="all, delete-orphan"),
    )


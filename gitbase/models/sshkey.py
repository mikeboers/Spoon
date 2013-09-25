import logging
import re

import bcrypt
import sqlalchemy as sa
import werkzeug as wz

from ..utils import debug
from . import app, db


log = logging.getLogger(__name__)


class SSHKey(db.Model):

    __tablename__ = 'ssh_keys'
    __table_args__ = dict(
        autoload=True,
        extend_existing=True,
    )

    owner = db.relationship('User', backref=db.backref('ssh_keys', cascade='save-update,delete,delete-orphan'))


    @property
    def cleaned(self):
        parts = self.data.strip().split()
        if parts[0] not in ('ssh-rsa', ):
            raise ValueError('unknown key format: %r' % parts[0])
        return '%s %s %s' % (parts[0], parts[1], self.owner.login)

import bcrypt
import sqlalchemy as sa
import werkzeug as wz


from ..core.flask import app, db


class User(db.Model):

    __tablename__ = 'users'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    # One-to-one to the repo that represents us.
    home = db.relationship('Group', backref=db.backref('owner', uselist=False))

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password):
        return self.password_hash and bcrypt.checkpw(password, self.password_hash)

    def is_authenticated(self):
        """For Flask-Login."""
        return True

    def is_active(self):
        """For Flask-Login."""
        return True

    def is_anonymous(self):
        """For Flask-Login."""
        return False

    def get_id(self):
        """For Flask-Login."""
        return self.name


class UserConverter(wz.routing.BaseConverter):

    def __init__(self, url_map):
        super(UserConverter, self).__init__(url_map)

    def to_python(self, name):
        try:
            user = User.query.filter_by(name=name).first()
            if user:
                return user
        except ValueError:
            pass
        raise wz.routing.ValidationError('user does not exist: %r' % name)

    def to_url(self, user):
        return user.name


app.url_map.converters['user'] = UserConverter





import bcrypt
import sqlalchemy as sa
import sqlalchemy.ext.mutable
import werkzeug as wz

from ..core.flask import app, db


class RoleSet(sa.types.TypeDecorator):

    impl = sa.String

    def process_bind_param(self, value, dialect):
        value = ','.join(str(x).strip() for x in sorted(value or ()))
        return value or None

    def process_result_value(self, value, dialect):
        value = (x.strip() for x in (value or '').split(','))
        value = set(x for x in value if x)
        return value


class MutableSet(sa.ext.mutable.Mutable, set):

    @classmethod
    def coerce(cls, name, value):
        return MutableSet(value or ())

    def _make_func(name):
        original = getattr(set, name)
        def _func(self, *args, **kwargs):
            try:
                return original(self, *args, **kwargs)
            finally:
                self.changed()
        return _func

    add = _make_func('add')
    clear = _make_func('clear')
    difference_update = _make_func('difference_update')
    discard = _make_func('discard')
    intersection_update = _make_func('intersection_update')
    pop = _make_func('pop')
    remove = _make_func('remove')
    symmetric_difference_update = _make_func('symmetric_difference_update')
    update = _make_func('update')

    del _make_func


class User(db.Model):

    __tablename__ = 'users'
    __table_args__ = dict(
        autoload=True,
        autoload_with=db.engine,
        extend_existing=True,
    )

    roles = db.Column('roles', MutableSet.as_mutable(RoleSet))

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
        return user.home.name if user.home else user.name

class HomelessUserConverter(UserConverter):

    def to_python(self, name):
        user = super(HomelessUserConverter, self).to_python(name)
        if user and user.home:
            raise wz.routing.ValidationError('user is not homeless: %r' % name)
        return user


app.url_map.converters['user'] = UserConverter
app.url_map.converters['homeless'] = HomelessUserConverter


from __future__ import absolute_import

import logging
from urllib import urlencode

import werkzeug as wz
import flask
from flask.ext.login import current_user

from . import utils


log = logging.getLogger(__name__)


class _Redirect(Exception):
    pass

class AuthManager(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.errorhandler(_Redirect)(lambda r: flask.redirect(r.args[0]))

    ACL = staticmethod(utils.ACL)
    can = staticmethod(utils.can)

    login_view = 'login'

    def assert_can(self, *args, **kwargs):

        flash_message = kwargs.pop('flash', 'You are not authorized for that action.')
        stealth = kwargs.pop('stealth', False)

        if not self.can(*args, **kwargs):
            if flash_message:
                flask.flash(flash_message, 'danger')
            if current_user.is_authenticated():
                flask.abort(403)
            elif not stealth and self.login_view:
                raise _Redirect(flask.url_for(self.login_view))
            else:
                flask.abort(401)


# Add some proxies
from . import predicates
for name in dir(predicates):
    if name[:1].isupper():
        setattr(AuthManager, name, getattr(predicates, name))


class AuthAppMixin(object):
    
    def __init__(self, *args, **kwargs):
        super(AuthAppMixin, self).__init__(*args, **kwargs)
        
        # Default ACL list that will be checked by an auth_predicate.
        self.router.__acl__ = [
            (True , '*', 'view'),
            (False, '*', '*'),
        ]
        
        # Here is the auth predicate that actually checks ACLs
        self.router.__auth_predicates__ = [HasPermission('view')]
    
    def setup_config(self):
        super(AuthAppMixin, self).setup_config()
        self.config.setdefaults(
            auth_login_url='/login',
            auth_cookie_name='user_id',
        )
        
    def _get_wsgi_app(self, environ):
        app = super(AuthAppMixin, self)._get_wsgi_app(environ)
        request = self.Request(environ)
        route = request.route_steps
        # We always have a route at this point if the route was successful.
        # We may not have one if it is doing a normalization redirection or
        # if a route was not found
        if route:
            for predicate in get_route_predicates(request.route_steps):
                if not predicate(request):
                    if request.user_id is None:
                        return self.authn_required_app
                    else:
                        return self.authz_denied_app
        return app
    
    def authn_required_app(self, request):
        return status.SeeOther(self.config.auth_login_url + '?' + urlencode(dict(
            redirect=request.url,
        )))
    
    def authz_denied_app(self, request):
        raise status.Forbidden()
    
    class RequestMixin(object):
        
        @property
        def user_id(self):
            return self.cookies.get(self.app.config.auth_cookie_name)
        
        @wz.utils.cached_property
        def user_principals(self):
            principals = set()
            if self.user_id is not None:
                principals.add(self.user_id)
            return principals
        
        def has_permission(self, permission):
            return check_acl_for_permission(self, get_route_acl(self.route_steps), permission)
    
    class ResponseMixin(object):
        
        def login(self, user_id):
            self.set_cookie(self.app.config.auth_cookie_name, user_id)
        
        def logout(self):
            self.delete_cookie(self.app.config.auth_cookie_name)








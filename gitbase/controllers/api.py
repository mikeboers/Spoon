import functools
import json

from . import *


def api(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        return json.dumps(func(*args, **kwargs)), 200, [('Content-Type', 'text/json')]
    return _func


# @app.route('/api/auth/check', methods=['POST'])
@api
def api_auth_check():

    try:
        perm = request.form['permission']
        type_ = request.form['type']
        id_ = int(request.form['id'])

        class_ = {
            'repo': Repo,
            'group': Group,
            'user': User,
        }[type_]

    except (KeyError, ValueError):
        return False

    obj = class_.query.get(id_)
    return auth.can(perm, obj)



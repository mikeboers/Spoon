from ..auth import dummy_anon

from . import *


@app.route('/debug/auth')
def debug_auth():
    if not (current_user.is_authenticated() and current_user.is_admin):
        abort(404)

    groups = list(Group.query.all())
    users = list(User.query.all())
    users.append(dummy_anon)

    return render_template('debug/auth.haml', groups=groups, users=users)

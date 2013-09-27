from ..auth import dummy_anon

from . import *


@app.route('/debug/auth')
@auth.ACL('''
    ALLOW ROOT http.get
    ALLOW OBSERVER http.get
    DENY ALL ALL
''')
def debug_auth():

    groups = list(Group.query.all())
    users = list(User.query.all())
    users.append(dummy_anon)

    return render_template('debug/auth.haml', groups=groups, users=users)

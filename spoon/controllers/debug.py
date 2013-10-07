from ..auth import dummy_anon

from . import *


@app.route('/debug/auth')
@auth.ACL('''
    ALLOW ROOT http.get
    ALLOW OBSERVER http.get
    DENY ANY ALL
''')
def debug_auth():

    groups = list(Account.query.all())
    users = [g for g in groups if not g.is_group]
    users.append(dummy_anon)

    return render_template('debug/auth.haml', groups=groups, users=users)

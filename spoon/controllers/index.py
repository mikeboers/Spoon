from . import *

@app.route('/')
def index():
    accounts = Account.query.options(sa.orm.joinedload('repos')).all()
    accounts = [g for g in accounts if auth.can('account.read', g)]
    accounts.sort(key=lambda g: g.name)
    return render_template('index.haml', accounts=accounts)

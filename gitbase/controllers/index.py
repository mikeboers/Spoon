from . import *

@app.route('/')
def index():

    groups = Group.query.options(sa.orm.joinedload('repos')).all()
    groups = [g for g in groups if auth.can('read', g)]
    
    return render_template('index.haml', groups=groups)

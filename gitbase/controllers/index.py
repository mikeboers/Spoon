from . import *

@app.route('/')
def index():
    groups = Group.query.options(sa.orm.joinedload('repos')).all()
    return render_template('index.haml', groups=groups)

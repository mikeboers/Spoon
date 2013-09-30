from . import *


@app.route('/<group:group>')
def group(group):
    return render_template('group/group.haml', group=group)

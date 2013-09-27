from . import *


@app.route('/<homeless:user>')
def user(user):
    return render_template('user.haml', user=user)


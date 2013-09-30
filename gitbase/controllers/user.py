from . import *


@app.route('/<homeless:user>')
def user(user):
    return render_template('user/user.haml', user=user)


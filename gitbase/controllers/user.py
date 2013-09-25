from . import *


@app.route('/users/<user:user>')
def user(user):
    return render_template('user.haml', user=user)


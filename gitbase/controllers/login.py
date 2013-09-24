import wtforms as wtf
from flask.ext.wtf import Form
from flask.ext.login import login_user, login_required, logout_user

from ..core.flask import login_manager

from . import *


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(login=userid).first()


class LoginForm(Form):

    username = wtf.TextField('Username', validators=[wtf.validators.Required()])
    password = wtf.PasswordField('Password', validators=[])



@app.route("/login", methods=["GET", "POST"])
def login():


    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(login=form.username.data).first()

        # TODO: check password
        if user:
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("User '%s' not found." % form.username.data, 'warning')

    else:
        flash('Please login.')

    return render_template("login.haml", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(request.args.get("next") or url_for("index"))
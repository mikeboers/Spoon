import wtforms as wtf
from flask.ext.wtf import Form
from flask.ext.login import login_user, login_required, logout_user

from ..core import login_manager

from . import *


@login_manager.user_loader
def load_user(userid):
    return Account.query.filter_by(name=userid).first()


class LoginForm(Form):

    username = wtf.TextField('Username', validators=[wtf.validators.Required()])
    password = wtf.PasswordField('Password', validators=[wtf.validators.Required()])



@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = Account.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):

            login_user(user, remember=True)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))

        else:
            flash("Username and password did not match.", 'warning')

    return render_template("login.haml", form=form)


@app.route('/login/su')
@requires_root
def login_switch_account():
    name = request.args.get('name')
    if name:
        account = Account.query.filter_by(name=name).first()
        if account:
            login_user(account)
            flash('Switched to "%s"' % name)
    return redirect(request.args.get("next") or url_for("index"))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(request.args.get("next") or url_for("index"))

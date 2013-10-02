import wtforms as wtf
from flask.ext.wtf import Form

from . import *


class NewRepoForm(Form):

    name = wtf.fields.TextField(validators=[wtf.validators.required()])
    public = wtf.fields.BooleanField(default=True)


@app.route('/<account:account>', methods=['GET', 'POST'])
def account(account):

    new_repo_form = NewRepoForm()

    if request.method == 'POST' and request.form.get('action') == 'account.delete':
        auth.assert_can('account.delete', account)
        if request.form.get('user_accepted_danger'):
            account.delete()
            flash('Deleted account "%s"' % account.name)
            return redirect(url_for('index'))
        else:
            flash('Javascript is required to delete groups.', 'danger')

    return render_template('account/account.haml', account=account, new_repo_form=new_repo_form)

import wtforms as wtf
from flask.ext.wtf import Form

from . import *


class NewRepoForm(Form):

    name = wtf.fields.TextField(validators=[wtf.validators.required()])
    public = wtf.fields.BooleanField(default=True)


class AccountMetaForm(Form):

    email = wtf.fields.TextField(validators=[wtf.validators.email()])
    url = wtf.fields.TextField(validators=[wtf.validators.url()])
    description = wtf.fields.TextAreaField()


@app.route('/<account:account>')
def account(account):
    return render_template('account/account.haml', account=account)


@app.route('/<account:account>/members')
def account_members(account):
    return render_template('account/members.haml', account=account)


@app.route('/<account:account>/admin', methods=['GET', 'POST'])
def account_admin(account):

    new_repo_form = NewRepoForm()
    account_meta_form = AccountMetaForm(obj=account)


    if request.method == 'POST' and request.form.get('action') == 'account.public_toggle':
        account.is_public = not account.is_public
        db.session.commit()
        if account.is_public:
            flash('Account is now public.', 'success')
        else:
            flash('Account is now private.', 'warning')

    if request.method == 'POST' and request.form.get('action') == 'account.meta.write':
        auth.assert_can('account.write', account)
        account_meta_form.populate_obj(account)
        flash('Updated account info.')
        db.session.commit()
        
    if request.method == 'POST' and request.form.get('action') == 'account.delete':
        auth.assert_can('account.delete', account)
        if request.form.get('user_accepted_danger'):
            account.delete()
            flash('Deleted account "%s"' % account.name)
            return redirect(url_for('index'))
        else:
            flash('Javascript is required to delete groups.', 'danger')

    return render_template('account/admin.haml',
        account=account,
        new_repo_form=new_repo_form,
        account_meta_form=account_meta_form,
    )


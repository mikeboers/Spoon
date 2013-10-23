import wtforms as wtf
from flask.ext.wtf import Form

from . import *
from ..models.sshkey import SSHKey


class NewRepoForm(Form):

    name = wtf.fields.TextField(validators=[wtf.validators.required()])
    public = wtf.fields.BooleanField(default=True)


class AddKeyForm(Form):

    encoded = wtf.fields.TextAreaField('New Key')


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
    add_key_form = AddKeyForm(formdata=None)

    if request.method == 'POST' and request.form.get('action') == 'account.public_toggle':
        auth.assert_can('account.write', account)
        account.is_public = not account.is_public
        db.session.commit()
        if account.is_public:
            flash('Account is now public.', 'success')
        else:
            flash('Account is now private.', 'warning')

    if request.method == 'POST' and request.form.get('action') == 'account.keys.create':
        auth.assert_can('account.write', account)
        encoded = request.form.get('encoded')
        try:
            key = SSHKey(data=encoded)
        except ValueError:
            flash('Malformed SSH Key', 'danger')
        else:
            account.ssh_keys.append(key)
            db.session.commit()
            flash('Added SSH key.')

    if request.method == 'POST' and request.form.get('action') == 'account.keys.delete':
        auth.assert_can('account.write', account)
        id_ = int(request.form.get('key.id'))
        account.ssh_keys = [x for x in account.ssh_keys if x.id != id_]
        flash('Deleted ssh key.')
        db.session.commit()

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
        add_key_form=add_key_form,
    )


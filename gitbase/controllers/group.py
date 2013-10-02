import wtforms as wtf
from flask.ext.wtf import Form

from . import *


class NewRepoForm(Form):

    name = wtf.fields.TextField(validators=[wtf.validators.required()])
    public = wtf.fields.BooleanField(default=True)


@app.route('/<account:group>', methods=['GET', 'POST'])
def group(group):

    new_repo_form = NewRepoForm()

    if request.method == 'POST' and request.form.get('action') == 'group.delete':
        auth.assert_can('group.delete', group)
        if request.form.get('user_accepted_danger'):
            group.delete()
            flash('Deleted group "%s"' % group.name)
            return redirect(url_for('index'))
        else:
            flash('Javascript is required to delete groups.', 'danger')

    return render_template('group/group.haml', group=group, new_repo_form=new_repo_form)

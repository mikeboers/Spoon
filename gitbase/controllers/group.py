from . import *


@app.route('/<group:group>', methods=['GET', 'POST'])
def group(group):

    if request.method == 'POST' and request.form.get('action') == 'group.delete':
        auth.assert_can('group.delete', group)
        if request.form.get('user_accepted_danger'):
            group.delete()
            flash('Deleted group "%s"' % group.name)
            return redirect(url_for('index'))
        else:
            flash('Javascript is required to delete groups.', 'danger')

    return render_template('group/group.haml', group=group)

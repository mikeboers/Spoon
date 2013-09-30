import wtforms as wtf
import wtforms.ext.sqlalchemy.fields
from markupsafe import Markup
from flask.ext.wtf import Form

from . import *


class NewGroupForm(Form):

    name = wtf.fields.TextField(validators=[wtf.validators.required()])
    public = wtf.fields.BooleanField()
    admin = wtf.ext.sqlalchemy.fields.QuerySelectField('Administrator',
        query_factory=lambda: User.query,
        get_label='name',
        get_pk=lambda x: x.id,
    )


acl = '''
    ALLOW ROOT ANY
    ALLOW OBSERVER http.get
    DENY ALL ALL
'''


@app.route('/cpanel', methods=['GET', 'POST'])
@auth.ACL(acl)
def cpanel():

    new_group_form = NewGroupForm()

    if request.form.get('action') == 'group.create' and new_group_form.validate():

        name = new_group_form.name.data.strip()
        group = Group.query.filter_by(name=name).first()
        if group:
            flash('Group "%s" already exists.', 'danger')
        else:

            group = Group(name=name, is_public=new_group_form.public.data)
            group.memberships.append(Membership(user=new_group_form.admin.data, is_admin=True))
            db.session.add(group)
            db.session.commit()
            flash(Markup('Group <a href="%s">%s</a> was created.') % (
                url_for('group', group=group),
                new_group_form.name.data,
            ))

            new_group_form = NewGroupForm(formdata=None)

    return render_template('cpanel/general.haml',
        new_group_form=new_group_form
    )


@app.route('/cpanel/users', methods=['GET', 'POST'])
@auth.ACL(acl)
def cpanel_users():
    users = User.query.all()
    return render_template('cpanel/users.haml', users=users)


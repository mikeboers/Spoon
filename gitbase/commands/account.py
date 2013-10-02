import itertools
import sys
from argparse import ArgumentParser

from ..core.flask import app, db
from ..models import Account, SSHKey, GroupMembership


def main():

    arg_parser = ArgumentParser()


    arg_parser.add_argument('-t', '--type')

    arg_parser.add_argument('-a', '--append', action='store_true')

    arg_parser.add_argument('-g', '--group', dest='groups', action='append')
    arg_parser.add_argument('-G', '--group-admin', dest='admin_groups', action='append')

    arg_parser.add_argument('-r', '--role', dest='roles', action='append')

    arg_parser.add_argument('-k', '--key', dest='keys', action='append')

    arg_parser.add_argument('-p', '--password')
    arg_parser.add_argument('--nopassword', action='store_true')

    arg_parser.add_argument('name')

    args = arg_parser.parse_args()

    account = Account.query.filter_by(name=args.name).first()
    if not account:
        account = Account(name=args.name)
        db.session.add(account)

    if args.type:
        if args.type == 'user':
            account.is_group = False
        elif args.type == 'group':
            account.is_group = True
        else:
            print 'type must be "account" or "group"'
            exit(3)

    if args.password:
        if account.is_group:
            print 'warning: setting password to group account'
        account.set_password(args.password)
    if args.nopassword:
        account.password_hash = None
        
    if (args.groups or args.admin_groups) and not args.append:
        account.groups = []

    combined_groups = list(itertools.chain(
        ((g, False) for g in args.groups or ()),
        ((g, True) for g in args.admin_groups or ()),
    ))

    if combined_groups and account.is_group:
        print 'warning: adding group memberships to group account'

    for group_name, is_admin in combined_groups:

        group_name = group_name.strip()
        account.groups = [m for m in account.groups if m.group.name != group_name]

        group = Account.query.filter_by(name=group_name).first()
        if group and not group.is_group:
            print 'Account', group_name, 'exists, but is not a group.'
            continue
        
        if not group:
            group = Account(name=group_name, is_group=True)
            db.session.add(group)

        account.groups.append(GroupMembership(user=account, group=group, is_admin=is_admin))

    if args.roles:
        if not args.append:
            account.roles = set()
        account.roles.update(args.roles)

    if args.keys:
        if account.is_group:
            print 'warning: adding SSH keys to group account'
        if not args.append:
            account.ssh_keys = []
        for raw_key in args.keys:
            ssh_key = SSHKey(data=raw_key)
            account.ssh_keys.append(ssh_key)

    db.session.commit()



def do_list(names):

    if names:
        users = User.query.filter(User.name.in_(names)).all()
    else:
        users = User.query.all()

    for i, account in enumerate(users):
        if i:
            print '---'
        print account.name
        print 'roles:', ', '.join(account.roles) or '<none>'
        print 'home:', account.home.name if account.home else '<none>'
        print 'groups:', ', '.join(m.group.name + ('(admin)' if m.is_admin else '') for m in account.memberships) or '<none>'


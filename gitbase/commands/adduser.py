import sys
from argparse import ArgumentParser

from ..core.flask import app, db
from ..models import User, Group, SSHKey


def main():

    arg_parser = ArgumentParser()

    arg_parser.add_argument('-e', '--edit', action='store_true')

    arg_parser.add_argument('--admin', action='store_true')
    arg_parser.add_argument('--no-admin', action='store_true')

    arg_parser.add_argument('-a', '--append', action='store_true')
    arg_parser.add_argument('-g', '-G', '--group', dest='groups', action='append')

    arg_parser.add_argument('-k', '--key', dest='keys', action='append')
    arg_parser.add_argument('-p', '--password')

    arg_parser.add_argument('login')

    args = arg_parser.parse_args()

    user = User.query.filter_by(login=args.login).first()

    if args.edit:
        if not user:
            print 'user not found'
            exit(1)
    elif user:
        print 'user already exists; did you mean to use --edit?'
        exit(2)
    else:
        user = User(login=args.login)
        db.session.add(user)

    if args.password:
        user.set_password(args.password)

    if args.admin:
        user.is_admin = True
    if args.no_admin:
        user.is_admin = False
    
    if args.groups:
        if not args.append:
            user.groups = []
        for group_name in args.groups:
            group = Group.query.filter_by(name=group_name).first()
            if not group:
                group = Group(name=group_name)
                db.session.add(group)
            if group not in user.groups:
                user.groups.append(group)

    if args.keys:
        if not args.append:
            user.ssh_keys = []
        for raw_key in args.keys:
            ssh_key = SSHKey(data=raw_key)
            user.ssh_keys.append(ssh_key)

    db.session.commit()

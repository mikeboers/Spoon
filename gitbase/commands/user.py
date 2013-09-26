import sys
from argparse import ArgumentParser

from ..core.flask import app, db
from ..models import User, Group, SSHKey, Membership


def main():

    arg_parser = ArgumentParser()

    arg_parser.add_argument('-e', '--edit', action='store_true')

    arg_parser.add_argument('--admin', action='store_true', default=None)
    arg_parser.add_argument('--no-admin', dest='admin', action='store_true', default=None)

    arg_parser.add_argument('-a', '--append', action='store_true')
    arg_parser.add_argument('-g', '--group', dest='groups', action='append')

    arg_parser.add_argument('--home')

    arg_parser.add_argument('-k', '--key', dest='keys', action='append')
    arg_parser.add_argument('-p', '--password')

    arg_parser.add_argument('name')

    args = arg_parser.parse_args()

    user = User.query.filter_by(name=args.name).first()

    if args.edit:
        if not user:
            print 'user not found'
            exit(1)
    elif user:
        print 'user already exists; did you mean to use --edit?'
        exit(2)
    else:
        user = User(name=args.name)
        db.session.add(user)

    if args.password:
        user.set_password(args.password)

    if args.admin is not None:
        user.is_admin = args.admin
    
    if args.groups:

        if not args.append:
            user.memberships = []

        for group_name in args.groups:

            group = Group.query.filter_by(name=group_name).first()
            if not group:
                group = Group(name=group_name)
                db.session.add(group)

            if any(m.group is group for m in user.memberships):
                continue

            db.session.add(Membership(user=user, group=group))

    if args.home:

        home = Group.query.filter_by(name=args.home).first()
        if not home:
            home = Group(name=args.home)
            db.session.add(home)
        user.home = home


    if args.keys:
        if not args.append:
            user.ssh_keys = []
        for raw_key in args.keys:
            ssh_key = SSHKey(data=raw_key)
            user.ssh_keys.append(ssh_key)

    db.session.commit()

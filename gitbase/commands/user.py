'''
usage: git-base-user add [options] name
   or: git-base-user edit [options] name
'''
__doc__ = __doc__.strip()

import itertools
import sys
from argparse import ArgumentParser

from ..core.flask import app, db
from ..models import User, Group, SSHKey, GroupMembership


def do_add(args, edit=False):

    arg_parser = ArgumentParser()

    arg_parser.add_argument('-a', '--append', action='store_true')

    arg_parser.add_argument('-g', '--group', dest='groups', action='append')
    arg_parser.add_argument('-G', '--group-admin', dest='admin_groups', action='append')
    arg_parser.add_argument('--home')

    arg_parser.add_argument('-r', '--role', dest='roles', action='append')

    arg_parser.add_argument('-k', '--key', dest='keys', action='append')

    arg_parser.add_argument('-p', '--password')
    arg_parser.add_argument('--nopassword', action='store_true')

    arg_parser.add_argument('name')

    args = arg_parser.parse_args(args)

    user = User.query.filter_by(name=args.name).first()

    if edit:
        if not user:
            print 'user not found'
            exit(1)
    elif user:
        print 'user already exists; did you mean to use `edit`?'
        exit(2)
    else:
        user = User(name=args.name)
        db.session.add(user)

    if args.password:
        user.set_password(args.password)
    if args.nopassword:
        user.password_hash = None
        
    if (args.groups or args.admin_groups) and not args.append:
        user.memberships = []

    group_iter = itertools.chain(
        ((g, False) for g in args.groups or ()),
        ((g, True) for g in args.admin_groups or ()),
    )
    for group_name, is_admin in group_iter:

        group_name = group_name.strip()
        user.memberships = [m for m in user.memberships if m.group.name != group_name]

        group = Group.query.filter_by(name=group_name).first()
        if not group:
            group = Group(name=group_name)
            db.session.add(group)

        user.memberships.append(GroupMembership(user=user, group=group, is_admin=is_admin))

    if args.home:

        home = Group.query.filter_by(name=args.home).first()
        if not home:
            home = Group(name=args.home)
            db.session.add(home)
        user.home = home

    if args.roles:
        if not args.append:
            user.roles = set()
        user.roles.update(args.roles)

    if args.keys:
        if not args.append:
            user.ssh_keys = []
        for raw_key in args.keys:
            ssh_key = SSHKey(data=raw_key)
            user.ssh_keys.append(ssh_key)

    db.session.commit()


def do_edit(args):
    do_add(args, edit=True)


def do_list(names):

    if names:
        users = User.query.filter(User.name.in_(names)).all()
    else:
        users = User.query.all()

    for i, user in enumerate(users):
        if i:
            print '---'
        print user.name
        print 'roles:', ', '.join(user.roles) or '<none>'
        print 'home:', user.home.name if user.home else '<none>'
        print 'groups:', ', '.join(m.group.name + ('(admin)' if m.is_admin else '') for m in user.memberships) or '<none>'

def main():


    if not len(sys.argv) > 1:
        print __doc__
        exit(1)
    command = globals().get('do_' + sys.argv[1])
    if not command:
        print __doc__
        exit(2)
    command(sys.argv[2:])


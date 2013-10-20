from argparse import ArgumentParser

from ..core import app
from ..models import sshkey


def main():

    arg_parser = ArgumentParser()
    arg_parser.add_argument('-r', '--rewrite', metavar='path', nargs='?', default=False, const=None)
    args = arg_parser.parse_args()

    if args.rewrite is not False:
        sshkey.rewrite_authorized_keys(args.rewrite)
    else:
        for chunk in sshkey.iter_authorized_keys():
            print chunk


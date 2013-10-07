import errno
import os
import sys


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def die(message, *args):
    code = 1
    if isinstance(message, int):
        code = message
        message = 'exited with code %s' % code
    elif args:
        message = message % args
    error(message)
    exit(code)


def stderr(*args):
    sys.stderr.write('%s\n' % ' '.join(str(x) for x in args))


def error(msg, *args):
    if args:
        msg = msg % args
    stderr('spoon:', msg)


debug = error


class classproperty(object):

    def __init__(self, getter):
        self._getter = getter

    def __get__(self, obj, cls_):
        return self._getter(cls_, obj)


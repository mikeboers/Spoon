'''
See: http://git-scm.com/book/en/Git-Internals-Transfer-Protocols#The-Dumb-Protocol
'''

import mimetypes

import pygit2

from . import *


PLAIN = [('Content-Type', 'text/plain')]


@app.route('/<repo:repo>/info/refs')
def dumb_refs(repo):
    out = []
    for ref in repo.git.listall_references():
        out.append('%s\t%s\n' % (repo.git.revparse_single(ref).hex, ref))
    return ''.join(out), 200, PLAIN


@app.route('/<repo:repo>/HEAD')
def dumb_head(repo):
    head = repo.git.head.get_object()
    for ref in repo.git.listall_references():
        if repo.git.revparse_single(ref).oid == head.oid:
            return 'ref: %s\n' % ref, 200, PLAIN
    return head.hex + '\n', 200, PLAIN


@app.route(r'/<repo:repo>/objects/<re("[0-9a-f]{2}"):prefix>/<re("[0-9a-f]{38}"):suffix>')
@app.route(r'/<repo:repo>/objects/<re("[0-9a-f]{2}"):prefix>/<re("[0-9a-f]{38}"):suffix><re("\.\w+"):ext>')
def raw_object(repo, prefix, suffix, ext=''):

    oid_hex = prefix + suffix
    blob = repo.git.get(oid_hex)

    if not blob:
        abort(404)

    if isinstance(blob, pygit2.Blob) and ext:

        if ext == '.md':
            type_ = 'text/x-markdown'
        else:
            type_ = mimetypes.types_map.get(ext, 'application/octet-stream')

        return blob.data, 200, [('Content-Type', type_)]


    else:
        return blob.read_raw(), 200, PLAIN

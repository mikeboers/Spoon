import mimetypes
import os

import pygit2

from . import *


@app.route('/<repo:repo>/tree/HEAD')
@app.route('/<repo:repo>/tree/<ref>')
@app.route('/<repo:repo>/tree/HEAD/<path:path>')
@app.route('/<repo:repo>/tree/<ref>/<path:path>')
def tree(repo, path='', ref='HEAD'):

    commit = repo.git.revparse_single(ref)
    entry = commit.tree[path] if path else commit.tree
    obj = repo.git[entry.oid]

    if isinstance(obj, pygit2.Tree):
        return render_template('tree/tree.haml', repo=repo, ref=ref, commit=commit, path=path, tree=obj)
    elif isinstance(obj, pygit2.Blob):
        return render_template('tree/blob.haml', repo=repo, ref=ref, commit=commit, path=path, blob=obj)

    abort(404)


@app.route(r'/<repo:repo>/raw/objects/<re("[0-9a-f]{2}"):prefix>/<re("[0-9a-f]{38}"):suffix>')
@app.route(r'/<repo:repo>/raw/objects/<re("[0-9a-f]{2}"):prefix>/<re("[0-9a-f]{38}"):suffix><re("\.\w+"):ext>')
def raw_object(repo, prefix, suffix, ext=''):

    oid_hex = prefix + suffix
    blob = repo.git.get(oid_hex)

    if not blob or not isinstance(blob, pygit2.Blob):
        abort(404)

    if ext == '.md':
        type_ = 'text/x-markdown'
    else:
        type_ = mimetypes.types_map.get(ext, 'application/octet-stream')

    return blob.data, 200, [('Content-Type', type_)]

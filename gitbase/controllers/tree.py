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
        return render_template('tree.haml', repo=repo, ref=ref, commit=commit, path=path, tree=obj)
    elif isinstance(obj, pygit2.Blob):
        return render_template('blob.haml', repo=repo, ref=ref, commit=commit, path=path, blob=obj)

    abort(404)


@app.route('/<repo:repo>/raw/HEAD/<path:path>')
@app.route('/<repo:repo>/raw/<ref>/<path:path>')
def raw_blob(repo, path, ref='HEAD'):

    commit = repo.git.revparse_single(ref)
    entry = commit.tree[path]
    obj = repo.git[entry.oid]

    if not isinstance(obj, pygit2.Blob):
        abort(404)

    if os.path.splitext(path)[1] == '.md':
        type_ = 'text/x-markdown'
    else:
        type_, encoding = mimetypes.guess_type(path)
        type_ = type_ or 'application/octet-stream'

    return obj.data, 200, [('Content-Type', type_)]

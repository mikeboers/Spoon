import mimetypes
import os

import pygit2

from . import *


@app.route('/<repo:repo>/tree/master')
@app.route('/<repo:repo>/tree/<ref>')
@app.route('/<repo:repo>/tree/master/<path:path>')
@app.route('/<repo:repo>/tree/<ref>/<path:path>')
def tree(repo, path='', ref='master'):

    commit = repo.git.revparse_single(ref)
    entry = commit.tree[path] if path else commit.tree
    obj = repo.git[entry.oid]

    if isinstance(obj, pygit2.Tree):
        return render_template('tree/tree.haml', repo=repo, ref=ref, commit=commit, path=path, tree=obj)
    elif isinstance(obj, pygit2.Blob):
        return render_template('tree/blob.haml', repo=repo, ref=ref, commit=commit, path=path, blob=obj)

    abort(404)





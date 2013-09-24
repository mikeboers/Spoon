import pygit2

from . import *


@app.route('/<repo:repo>/tree/HEAD/<path:path>')
@app.route('/<repo:repo>/tree/<ref>/<path:path>')
def tree(repo, path, ref='HEAD'):

    commit = repo.git.revparse_single(ref)
    entry = commit.tree[path]
    obj = repo.git[entry.oid]

    if isinstance(obj, pygit2.Tree):
        return render_template('tree.haml', repo=repo, commit=commit, path=path, tree=obj)
    elif isinstance(obj, pygit2.Blob):
        return render_template('blob.haml', repo=repo, commit=commit, path=path, blob=obj)

    abort(404)


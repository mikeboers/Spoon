import pygit2

from . import *


@app.route('/<repo:repo>/<path:path>')
def tree(repo, path):

    entry = repo.git.head.get_object().tree[path]
    obj = repo.git[entry.oid]
    if isinstance(obj, pygit2.Tree):
        return render_template('tree.haml', repo=repo, path=path, tree=obj)
    elif isinstance(obj, pygit2.Blob):
        return render_template('blob.haml', repo=repo, path=path, blob=obj)

    abort(404)


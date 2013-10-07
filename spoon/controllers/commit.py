import pygit2

from . import *


@app.route('/<repo:repo>/diff/<commit>')
def commit(repo, commit):

    try:
        commit = repo.git[commit]
    except KeyError:
        abort(404)

    if not isinstance(commit, pygit2.Commit):
        abort(404)

    return render_template('commit/commit.haml', repo=repo, commit=commit)



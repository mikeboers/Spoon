import itertools
import pygit2 as git

from . import *


@app.route('/<repo:repo>')
def repo(repo):
    return render_template('repo.haml', repo=repo, group=repo.group)


@app.route('/<repo:repo>/commits')
def commits(repo):

    if 'after' in request.args:
        try:
            head = repo.git.revparse_single(request.args['after'])
        except git.GitError:
            abort(404)
    else:
        try:
            head = repo.git.head.get_object()
        except git.GitError:
            head = None

    if not head:
        return render_template('commits.haml', repo=repo)

    # Getting the set of commits and the next one are easy. Getting the
    # start of the previous set? Not so much...
    walker = repo.git.walk(head.oid, git.GIT_SORT_TOPOLOGICAL)
    commits = list(itertools.islice(walker, app.config['COMMITS_PER_PAGE']))
    next_commit = next(walker, None)

    # We need to start at the HEAD and walk until we find it.
    prev_commits = []
    for commit in repo.git.walk(repo.git.head.get_object().oid, git.GIT_SORT_TOPOLOGICAL):
        if commit.oid == head.oid:
            break
        prev_commits.append(commit)
    prev_commits = prev_commits[-50:]
    prev_commit = prev_commits[0] if prev_commits else None

    hex_to_refs = {head.oid: [('head', 'HEAD')]}
    for ref in repo.git.listall_references():
        hex_to_refs.setdefault(repo.git.revparse_single(ref).oid, []).append(ref.split('/', 2)[1:])

    return render_template('commits.haml',
        repo=repo,
        head=head,
        commits=commits,
        next_commit=next_commit,
        prev_commit=prev_commit,
        hex_to_refs=hex_to_refs,
    )

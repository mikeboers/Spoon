import itertools

import pygit2 as git

from . import *


@app.route('/<repo:repo>')
def repo(repo):
    return render_template('repo/repo.haml', repo=repo)

@app.route('/<repo:repo>/admin', methods=['GET', 'POST'])
def repo_admin(repo):

    if request.method == 'POST' and request.form.get('action') == 'repo.public_toggle':
        repo.is_public = not repo.is_public
        db.session.commit()
        if repo.is_public:
            flash('Repo is now public.', 'success')
        else:
            flash('Repo is now private.', 'warning')

    if request.method == 'POST' and request.form.get('action') == 'repo.delete':
        auth.assert_can('repo.delete', repo)
        if request.form.get('user_accepted_danger'):
            repo.delete()
            flash('Deleted repo "%s/%s"' % (repo.account.name, repo.name))
            return redirect(url_for('account', account=repo.account))
        else:
            flash('Javascript is required to delete repos.', 'danger')

    return render_template('repo/admin.haml', repo=repo)

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
        return render_template('commit/list.haml', repo=repo)

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

    return render_template('commit/list.haml',
        repo=repo,
        head=head,
        commits=commits,
        next_commit=next_commit,
        prev_commit=prev_commit,
        hex_to_refs=hex_to_refs,
    )

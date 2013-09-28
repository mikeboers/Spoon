from . import *


@app.route('/<repo:repo>')
def repo(repo):
    return render_template('repo.haml', repo=repo, group=repo.group)


@app.route('/<repo:repo>/commits')
def commits(repo):
    return render_template('commits.haml', repo=repo)

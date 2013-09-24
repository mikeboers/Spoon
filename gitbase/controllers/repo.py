from . import *


@app.route('/<repo:repo>')
def repo(repo):

    # auth.assert_can('read', repo, repo=repo)
    
    return render_template('repo.haml', repo=repo, group=repo.group)

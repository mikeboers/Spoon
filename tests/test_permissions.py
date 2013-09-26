from . import *


class TestPermissions(TestCase):

    def test_anonymous_user_with_private_repo_in_public_group(self):

        user = dummy_anon
        repo = Repo(name='private_repo', is_public=False)
        group = Group(name='public_group', is_public=True)
        group.repos.append(repo)

        ctx = dict(current_user=user, repo=repo, group=group)

        # I would also like to test for not group.read on the repo, but
        # they don't work like that... yet.
        self.assertTrue(auth.can('group.read', group, **ctx))
        self.assertFalse(auth.can('repo.read', repo, **ctx))

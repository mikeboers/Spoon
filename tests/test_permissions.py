from . import *


class TestPermissions(TestCase):

    needs_context = True
    
    def test_wheel(self):

        repo = Repo(name='private_repo', is_public=False)
        account = Account(name='public_group', is_public=True, is_group=True)

        # The wheel can do anything it wants.
        self.assertTrue(auth.can('does.not.exist', repo, user=dummy_admin))
        self.assertTrue(auth.can('does.not.exist', account, user=dummy_admin))

    def test_private_repo_in_public_group(self):

        repo = Repo(name='private_repo', is_public=False)
        account = Account(name='public_group', is_public=True, is_group=True)
        account.repos.append(repo)
        another_user = Account(name='another_user', roles=set(), id=1)
        member = Account(name='group_member', roles=set(), id=2)
        account.members.append(GroupMembership(user=member))

        # Anonymous user.
        ctx = dict(user=dummy_anon, account=account, repo=repo)
        self.assertTrue(auth.can('account.read', account, **ctx))
        self.assertFalse(auth.can('repo.read', repo, **ctx))
        self.assertFalse(auth.can('repo.write', repo, **ctx))

        # Authenticated user.
        ctx = dict(user=dummy_anon, account=account, repo=repo)
        self.assertTrue(auth.can('account.read', account, **ctx))
        self.assertFalse(auth.can('repo.read', repo, **ctx))
        self.assertFalse(auth.can('repo.write', repo, **ctx))

        # Group member.
        ctx = dict(user=member, account=account, repo=repo)
        self.assertTrue(auth.can('account.read', account, **ctx))
        self.assertTrue(auth.can('repo.read', repo, **ctx))
        self.assertTrue(auth.can('repo.write', repo, **ctx))

    def test_public_repo_in_private_group(self):

        repo = Repo(name='private_repo', is_public=True)
        account = Account(name='public_group', is_public=False, is_group=True)
        account.repos.append(repo)
        another_user = Account(name='another_user', roles=set(), id=1)
        member = Account(name='group_member', roles=set())
        account.members.append(GroupMembership(user=member))

        # Anonymous user.
        ctx = dict(user=dummy_anon, account=account, repo=repo)
        self.assertFalse(auth.can('account.read', account, **ctx))
        self.assertFalse(auth.can('repo.read', repo, **ctx))
        self.assertFalse(auth.can('repo.write', repo, **ctx))

        # Authenticated user.
        ctx = dict(user=another_user, account=account, repo=repo)
        self.assertFalse(auth.can('account.read', account, **ctx))
        self.assertFalse(auth.can('repo.read', repo, **ctx))
        self.assertFalse(auth.can('repo.write', repo, **ctx))

        # Group member.
        ctx = dict(user=member, account=account, repo=repo)
        self.assertTrue(auth.can('account.read', account, **ctx))
        self.assertTrue(auth.can('repo.read', repo, **ctx))
        self.assertTrue(auth.can('repo.write', repo, **ctx))


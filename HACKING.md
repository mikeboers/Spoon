
Accounts for Users and Groups
=============================

Users and groups are both represented by a single class, the `Account`. The different is made via a single `account.is_group` flag.

The general differences are:
    
- End users may login to a user account (i.e. where `not account.is_public`).
- Group accounts may contain repositories.
- User accounts may contain repositories only if they have the `publisher` role.

Sometimes, I may have referred to these as `user` and `group`, but I am trying to remove as much of that as possible. Generally, they should be called `account` unless they are the account of the active user, in which case they may be called `user`.

Account relationships are exposed via `members` (for user account members of a group account) and `groups` (group accounts that the given user account is a member of).

It is technically possible to have members of a user group, and also to set passwords on a group account, but it is not advisable as the code generally does not consider this.


Role Sets
=========

Sets of roles are represented by a `String` column, where the individual roles are delimited and terminated by a `|` (vertical bar).

For example, a user account with the "observer" and "publisher" roles would look like:

    |observer|publisher|

This representation was chosen for easy querying via the SQL `LIKE` expression:

    SELECT * FROM accounts WHERE role LIKE "%|observer|%";

Known roles include:

- `wheel`: an administrator; generally they can do anything.
- `observer`: able to see much of the inner workings, but unable to directly affect them.


Permissions
===========

The following are some permissions that are checked:

- `account.read`: is the account (and its contents) visible to the user?
- `account.write`: may the user modify the account by editing metadata (e.g description)?
- `repo.create`: may the user create a new repo in the account?
- `repo.read`: is the repo (and its contents) visible to the user?
- `repo.write`: may the user push (and merge or force push) into the repo?
- `repo.delete`: may the user delete the repo.

A permission on an object usually implies lesser permissions of the same class. E.g. a user with `repo.delete` may also `repo.write` and `repo.read`.


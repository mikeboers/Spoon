
Accounts for Users and Groups
=============================

Users and groups are both represented by a single class, the `Account`. The different is made via a single `account.is_group` flag.

The general differences are:
    
- End users may login to a user account (i.e. where `not account.is_public`).
- Group accounts may contain repositories.
- User accounts may contain repositories only if they have the `publisher` role.

Despite these two objects being represented by the same type, usually the code will refer to an instance as either `user` or `group`. This includes permissions, in which `user` is the user performing the action, and `group` is the account that should be treated as the repo container.


Role Sets
=========

Sets of roles are represented by a `String` column, where the individual roles are delimited and terminated by a `|` (vertical bar).

For example, a user account with the "observer" and "publisher" roles would look like:

    |observer|publisher|

This representation was chosen for easy querying via the SQL `LIKE` expression:

    SELECT * FROM accounts WHERE role LIKE "%|observer|%";


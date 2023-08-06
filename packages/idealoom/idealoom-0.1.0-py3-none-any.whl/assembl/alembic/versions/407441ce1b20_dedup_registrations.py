"""dedup_registrations

Revision ID: 407441ce1b20
Revises: bb2849f2c085
Create Date: 2018-06-03 15:48:35.931332

"""

# revision identifiers, used by Alembic.
revision = '407441ce1b20'
down_revision = 'bb2849f2c085'

from functools import reduce

from alembic import context, op
import sqlalchemy as sa
import transaction
from collections import defaultdict
from operator import or_
from sqlalchemy.orm import joinedload

from assembl.lib import config


def upgrade(pyramid_env):
    with context.begin_transaction():
        pass

    # Do stuff with the app's models here.
    from assembl import models as m
    db = m.get_session_maker()()
    with transaction.manager:
        bymail = defaultdict(list)
        emails = db.query(m.EmailAccount).join(
            m.User, m.User.id == m.EmailAccount.profile_id).options(
            joinedload(m.EmailAccount.profile)).all()
        for email in emails:
            bymail[email.email].append(email)

        # all emails with duplicate accounts
        duplicates = [v for v in bymail.values() if len(v) > 1]

        def order(acc):
            return (acc.verified, acc.profile, acc.profile.id)

        for dups in duplicates:
            # Make the profile verified iff one verified account
            for acc in dups:
                acc.profile.verified = reduce(or_, [
                    a.verified for a in acc.profile.accounts])
            # the "best" (verified, latest) will be last
            dups.sort(key=order)
            for acc in dups[:-1]:
                assert not acc.verified
            acc = dups[-1]

        for dups in duplicates:
            # keep last profile
            keep_profile = dups[-1].profile_id
            for acc in dups[:-1]:
                acc.delete()
                # i.e. delete profile if not last.
                # There were cases of 2 accounts to one profile, one verified
                if acc.profile_id != keep_profile:
                    acc.profile.delete()


def downgrade(pyramid_env):
    pass

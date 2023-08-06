from __future__ import print_function
from datetime import datetime

import pytest
from pyramid import testing
from pyramid.threadlocal import manager

from assembl.auth import R_PARTICIPANT
from assembl.lib.config import get_config
from ..utils import PyramidWebTestRequest


@pytest.fixture(scope="function")
def participant1_user(request, test_session, discussion):
    """A User fixture with R_PARTICIPANT role"""

    from assembl.models import User, UserRole, Role, EmailAccount
    u = User(name=u"A. Barking Loon", type="user", password="password",
             verified=True, last_idealoom_login=datetime.utcnow())
    email = EmailAccount(email="abloon@gmail.com", profile=u, verified=True)
    test_session.add(u)
    r = Role.get_role(R_PARTICIPANT, test_session)
    ur = UserRole(user=u, role=r)
    test_session.add(ur)
    u.subscribe(discussion)
    test_session.flush()

    def fin():
        print("finalizer participant1_user")
        test_session.delete(u)
        test_session.flush()
    request.addfinalizer(fin)
    return u


@pytest.fixture(scope="function")
def test_participant1_webrequest(request, participant1_user, test_app_no_perm):
    """A Pyramid request fixture with an ADMIN user authorized"""
    req = PyramidWebTestRequest.blank('/', method="GET")
    req.authenticated_userid = participant1_user.id

    def fin():
        # The request was not called
        manager.pop()
    request.addfinalizer(fin)
    return req


@pytest.fixture(scope="function")
def test_app_participant1(request, participant1_user, test_app_no_perm):
    """A configured IdeaLoom fixture with permissions
    and an participant1 user logged in"""

    config = testing.setUp(
        registry=test_app_no_perm.app.registry,
        settings=get_config(),
    )
    dummy_policy = config.testing_securitypolicy(
        userid=participant1_user.id, permissive=True)
    config.set_authorization_policy(dummy_policy)
    config.set_authentication_policy(dummy_policy)
    return test_app_no_perm


@pytest.fixture(scope="function")
def participant2_user(request, test_session):
    """A User fixture with R_PARTICIPANT role"""

    from assembl.models import User, UserRole, Role
    u = User(name=u"James T. Expert", type="user",
             last_idealoom_login=datetime.utcnow())
    test_session.add(u)
    r = Role.get_role(R_PARTICIPANT, test_session)
    ur = UserRole(user=u, role=r)
    test_session.add(ur)
    test_session.flush()

    def fin():
        print("finalizer participant2_user")
        test_session.delete(u)
        test_session.flush()
    request.addfinalizer(fin)
    return u

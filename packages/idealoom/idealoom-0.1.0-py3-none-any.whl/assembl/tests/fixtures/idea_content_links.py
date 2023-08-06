from __future__ import print_function
import pytest


@pytest.fixture(scope="function")
def criterion_1(request, discussion, subidea_1, test_session):
    """An Idea fixture with IdeaLink to subidea_1"""

    from assembl.models import Idea, IdeaLink, LangString
    i = Idea(title=LangString.create(u"cost", 'en'),
             discussion=discussion)
    test_session.add(i)
    l_1_11 = IdeaLink(source=subidea_1, target=i)
    test_session.add(l_1_11)
    test_session.flush()

    def fin():
        print("finalizer criterion_1")
        test_session.delete(l_1_11)
        test_session.delete(i)
        test_session.flush()
    request.addfinalizer(fin)
    return i


@pytest.fixture(scope="function")
def criterion_2(request, discussion, subidea_1, test_session):
    """An Idea fixture with IdeaLink to subidea_1"""

    from assembl.models import Idea, IdeaLink, LangString
    i = Idea(title=LangString.create(u"quality", 'en'),
             discussion=discussion)
    test_session.add(i)
    l_1_11 = IdeaLink(source=subidea_1, target=i)
    test_session.add(l_1_11)
    test_session.flush()

    def fin():
        print("finalizer criterion_2")
        test_session.delete(l_1_11)
        test_session.delete(i)
        test_session.flush()
    request.addfinalizer(fin)
    return i


@pytest.fixture(scope="function")
def criterion_3(request, discussion, subidea_1, test_session):
    """An Idea fixture with IdeaLink to subidea_1"""

    from assembl.models import Idea, IdeaLink, LangString
    i = Idea(title=LangString.create(u"time", 'en'),
             discussion=discussion)
    test_session.add(i)
    l_1_11 = IdeaLink(source=subidea_1, target=i)
    test_session.add(l_1_11)
    test_session.flush()

    def fin():
        print("finalizer criterion_3")
        test_session.delete(l_1_11)
        test_session.delete(i)
        test_session.flush()
    request.addfinalizer(fin)
    return i


@pytest.fixture(scope="function")
def synthesis_1(request, discussion, subidea_1, subidea_1_1, test_session):
    """A Synthesis fixture"""

    from assembl.models import Synthesis, SubGraphIdeaAssociation,\
        SubGraphIdeaLinkAssociation
    s = Synthesis(discussion=discussion)
    test_session.add(s)
    i1_a = SubGraphIdeaAssociation(sub_graph=s, idea=subidea_1)
    test_session.add(i1_a)
    i11_a = SubGraphIdeaAssociation(sub_graph=s, idea=subidea_1_1)
    test_session.add(i11_a)
    l_1_11 = subidea_1_1.source_links[0]
    l_1_11_a = SubGraphIdeaLinkAssociation(sub_graph=s, idea_link=l_1_11)
    test_session.add(l_1_11_a)
    test_session.flush()

    def fin():
        print("finalizer synthesis_1")
        test_session.delete(l_1_11_a)
        test_session.delete(i11_a)
        test_session.delete(i1_a)
        test_session.delete(s)
        test_session.flush()
    request.addfinalizer(fin)

    return s


@pytest.fixture(scope="function")
def extract_post_1_to_subidea_1_1(
        request, participant2_user, reply_post_1,
        subidea_1_1, discussion, test_session):
    """ Links reply_post_1 to subidea_1_1 """

    from assembl.models import Extract
    e = Extract(
        annotation_text=u"body",
        creator=participant2_user,
        owner=participant2_user,
        content=reply_post_1,
        idea_id=subidea_1_1.id,  # strange bug: Using idea directly fails
        discussion=discussion)
    test_session.add(e)
    test_session.flush()

    def fin():
        print("finalizer extract_post_1_to_subidea_1_1")
        test_session.delete(e)
        test_session.flush()
    request.addfinalizer(fin)
    return e


@pytest.fixture(scope="function")
def jack_layton_linked_discussion(
        request, test_session, jack_layton_mailbox, subidea_1, subidea_1_1,
        subidea_1_1_1, subidea_1_1_1_1, subidea_1_1_1_1_1, subidea_1_1_1_1_2,
        subidea_1_1_1_1_2_1, subidea_1_1_1_1_2_2, subidea_1_2, subidea_1_2_1,
        admin_user):
    """A Discussion fixture with ideas and idea links"""

    jack_layton_mailbox.do_import_content(jack_layton_mailbox, True)
    from assembl.models import (
        Post, IdeaContentPositiveLink, IdeaContentNegativeLink)
    posts = test_session.query(Post).order_by(Post.creation_date).all()
    posts.insert(0, None)  # We are using 1-offset indices below.
    links = [
        IdeaContentPositiveLink(idea=subidea_1, content=posts[1], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1, content=posts[5], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1, content=posts[16], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1, content=posts[6], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1, content=posts[18], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1, content=posts[8], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1_1_1_1, content=posts[16], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1_1, content=posts[18], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1_1, content=posts[15], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1_1_1_1_1, content=posts[16], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1_2, content=posts[19], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1_2_1, content=posts[19], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_1_1_1_2_2, content=posts[20], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_2, content=posts[4], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1_2, content=posts[16], creator=admin_user),
        IdeaContentPositiveLink(idea=subidea_1_2_1, content=posts[4], creator=admin_user),
        IdeaContentNegativeLink(idea=subidea_1_2_1, content=posts[16], creator=admin_user),
    ]
    for link in links:
        test_session.add(link)
    test_session.flush()

    def fin():
        for link in links:
            test_session.delete(link)
        test_session.flush()
    request.addfinalizer(fin)
    return links

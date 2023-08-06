# -*- coding: utf-8 -*-
"""Defining the idea and links between ideas."""

from builtins import str
from builtins import object
from itertools import chain, groupby
from collections import defaultdict
from abc import ABCMeta, abstractmethod
from datetime import datetime
import threading

from future.utils import as_native_str
from ..lib.clean_input import sanitize_text
from rdflib import URIRef
from sqlalchemy.orm import (
    relationship, backref, aliased, contains_eager, joinedload, deferred,
    column_property, with_polymorphic, remote, foreign)
from sqlalchemy.orm.attributes import NO_VALUE
from sqlalchemy.sql import text, column
from sqlalchemy.sql.expression import union, bindparam, literal_column

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    Unicode,
    Float,
    UnicodeText,
    DateTime,
    ForeignKey,
    inspect,
    select,
    func,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqla_rdfbridge.mapping import IriClass, PatternIriClass
from pyramid.i18n import TranslationStringFactory

from ..lib.utils import get_global_base_url
from ..nlp.wordcounter import WordCounter
from . import DiscussionBoundBase, HistoryMixinWithOrigin
from .discussion import Discussion
from .uriref import URIRefDb
from ..semantic.virtuoso_mapping import QuadMapPatternS
from ..auth import (
    CrudPermissions, P_READ, P_ADMIN_DISC, P_EDIT_IDEA,
    P_ADD_IDEA)
from .langstrings import LangString, LangStringEntry
from ..semantic.namespaces import (
    SIOC, IDEA, ASSEMBL, QUADNAMES, FOAF, RDF, VirtRDF)
from ..lib.sqla import CrudOperation
from ..lib.model_watcher import get_model_watcher
from assembl.views.traversal import (
    AbstractCollectionDefinition, RelationCollectionDefinition,
    collection_creation_side_effects, InstanceContext)
from future.utils import with_metaclass

if DiscussionBoundBase.using_virtuoso:
    from virtuoso.alchemy import Timestamp
else:
    from sqlalchemy.types import TIMESTAMP as Timestamp


_ = TranslationStringFactory('assembl')


class defaultdictlist(defaultdict):
    """A defaultdict of lists."""
    def __init__(self):
        super(defaultdictlist, self).__init__(list)


class IdeaVisitor(with_metaclass(ABCMeta, object)):
    """A Visitor_ for the structure of :py:class:`Idea`

    The visit is started by :py:meth:`Idea.visit_ideas_depth_first`,
    :py:meth:`Idea.visit_ideas_breadth_first` or
    :py:meth:`Idea.visit_idea_ids_depth_first`

    .. _Visitor: https://sourcemaking.com/design_patterns/visitor
    """
    CUT_VISIT = object()

    @abstractmethod
    def visit_idea(self, idea, level, prev_result):
        pass

    def end_visit(self, idea, level, result, child_results):
        return result


class IdeaLinkVisitor(with_metaclass(ABCMeta, object)):
    """A Visitor for the structure of :py:class:`IdeaLink`"""
    CUT_VISIT = object()

    @abstractmethod
    def visit_link(self, link):
        pass


class AppendingVisitor(IdeaVisitor):
    """A Visitor that appends visit results to a list"""

    def __init__(self):
        self.ideas = []

    def visit_idea(self, idea, level, prev_result):
        self.ideas.append(idea)
        return self.ideas


class WordCountVisitor(IdeaVisitor):
    """A Visitor that counts words related to an idea"""
    def __init__(self, langs, count_posts=True):
        self.counter = WordCounter(langs)
        self.count_posts = True

    def cleantext(self, text):
        return sanitize_text(text)

    def visit_idea(self, idea, level, prev_result):
        if idea.short_title:
            self.counter.add_text(self.cleantext(idea.short_title), 2)
        if idea.long_title:
            self.counter.add_text(self.cleantext(idea.long_title))
        if idea.definition:
            self.counter.add_text(self.cleantext(idea.definition))
        if self.count_posts and level == 0:
            from .generic import Content
            query = idea.db.query(Content)
            related = idea.get_related_posts_query(True)
            query = query.join(related, Content.id == related.c.post_id
                ).filter(Content.hidden==False,
                         Content.tombstone_condition()).options(
                    Content.subqueryload_options())
            titles = set()
            # TODO maparent: Group langstrings by language.
            for content in query:
                body = content.body.first_original().value
                self.counter.add_text(self.cleantext(body), 0.5)
                title = content.subject.first_original().value
                title = self.cleantext(title)
                if title not in titles:
                    self.counter.add_text(title)
                    titles.add(title)

    def best(self, num=8):
        return self.counter.best(num)


class Idea(HistoryMixinWithOrigin, DiscussionBoundBase):
    """
    An idea (or concept) distilled from the conversation flux.
    """
    __tablename__ = "idea"
    __external_typename = "GenericIdeaNode"
    ORPHAN_POSTS_IDEA_ID = 'orphan_posts'
    sqla_type = Column(String(60), nullable=False)
    rdf_type_id = Column(
        Integer, ForeignKey(URIRefDb.id),
        server_default=str(URIRefDb.index_of(IDEA.GenericIdeaNode)))

    title_id = Column(
        Integer(), ForeignKey(LangString.id))
    synthesis_title_id = Column(
        Integer(), ForeignKey(LangString.id))
    description_id = Column(
        Integer(), ForeignKey(LangString.id))
    title = relationship(
        LangString,
        lazy="joined",
        primaryjoin=title_id == LangString.id,
        backref=backref("idea_from_title", lazy="dynamic"),
        cascade="all")
    synthesis_title = relationship(
        LangString,
        lazy="joined",
        primaryjoin=synthesis_title_id == LangString.id,
        backref=backref("idea_from_synthesis_title", lazy="dynamic"),
        cascade="all")
    description = relationship(
        LangString,
        lazy="joined",
        primaryjoin=description_id == LangString.id,
        backref=backref("idea_from_description", lazy="dynamic"),
        cascade="all")
    hidden = Column(Boolean, server_default='0')
    last_modified = Column(Timestamp)
    # TODO: Make this autoupdate on change. see
    # http://stackoverflow.com/questions/1035980/update-timestamp-when-row-is-updated-in-postgresql

    # temporary placeholders
    @property
    def definition(self):
        if self.description_id:
            return self.description.first_original().value
        return ""

    @property
    def long_title(self):
        if self.synthesis_title_id:
            return self.synthesis_title.first_original().value
        return ""

    @property
    def short_title(self):
        if self.title_id:
            return self.title.first_original().value
        return ""

    discussion_id = Column(Integer, ForeignKey(
        'discussion.id',
        ondelete='CASCADE',
        onupdate='CASCADE'),
        nullable=False,
        index=True,
        info={'rdf': QuadMapPatternS(None, SIOC.has_container)})

    discussion = relationship(
        Discussion,
        backref=backref(
            'ideas', order_by="Idea.creation_date",
            primaryjoin="and_(Idea.discussion_id==Discussion.id, "
                        "Idea.tombstone_date == None)"),
        info={'rdf': QuadMapPatternS(None, ASSEMBL.in_conversation)}
    )

    discussion_ts = relationship(
        Discussion,
        backref=backref(
            'ideas_ts', order_by="Idea.creation_date",
            cascade="all, delete-orphan")
    )

    title_entries = relationship(
        LangStringEntry, viewonly=True, uselist=True,
        primaryjoin=foreign(title_id)==remote(LangStringEntry.langstring_id))

    description_entries = relationship(
        LangStringEntry, viewonly=True, uselist=True,
        primaryjoin=foreign(description_id)==remote(
            LangStringEntry.langstring_id))

    links = relationship(
        "IdeaLink", viewonly=True, uselist=True,
        primaryjoin="""(IdeaLink.tombstone_date == None) & (
            (IdeaLink.source_id==Idea.id)|(IdeaLink.target_id==Idea.id))""")

    #widget_id = deferred(Column(Integer, ForeignKey('widget.id')))
    #widget = relationship("Widget", backref=backref('ideas', order_by=creation_date))

    __mapper_args__ = {
        'polymorphic_identity': 'idea',
        'polymorphic_on': sqla_type,
        # Not worth it for now, as the only other class is RootIdea, and there
        # is only one per discussion - benoitg 2013-12-23
        #'with_polymorphic': '*'
    }

    def populate_from_context(self, context):
        if not(self.discussion or self.discussion_id):
            self.discussion = context.get_instance_of_class(Discussion)
        super(Idea, self).populate_from_context(context)

    @classmethod
    def special_quad_patterns(cls, alias_maker, discussion_id):
        discussion_alias = alias_maker.get_reln_alias(cls.discussion)
        return [
            QuadMapPatternS(
                None, RDF.type,
                IriClass(VirtRDF.QNAME_ID).apply(Idea.rdf_type_db.val),
                name=QUADNAMES.class_Idea_class),
            QuadMapPatternS(
                None, FOAF.homepage,
                PatternIriClass(
                    QUADNAMES.idea_external_link_iri,
                    # TODO: Use discussion.get_base_url.
                    # This should be computed outside the DB.
                    get_global_base_url() + '/%s/idea/local:' +
                    cls.external_typename_with_inheritance() + '/%d', None,
                    ('slug', Unicode, False), ('id', Integer, False)).apply(
                    discussion_alias.slug, cls.id),
                name=QUADNAMES.idea_external_link_map)
        ]

    parents = association_proxy(
        'source_links', 'source',
        creator=lambda idea: IdeaLink(source=idea))

    parents_ts = association_proxy(
        'source_links_ts', 'source_ts',
        creator=lambda idea: IdeaLink(source=idea))

    children = association_proxy(
        'target_links', 'target',
        creator=lambda idea: IdeaLink(target=idea))

    rdf_type_db = relationship(URIRefDb)

    @property
    def rdf_type_url(self):
        return self.rdf_type_db.val

    @rdf_type_url.setter
    def rdf_type_url(self, val):
        val = URIRefDb.get_or_create(val, self.db)
        if val != self.rdf_type_db:
            self.rdf_type_db = val
            self.applyTypeRules()

    @property
    def rdf_type_curie(self):
        return self.rdf_type_db.as_curie

    @rdf_type_curie.setter
    def rdf_type_curie(self, val):
        val = URIRefDb.get_or_create_from_curie(val, self.db)
        if val != self.rdf_type_db:
            self.rdf_type_db = val
            self.applyTypeRules()

    @property
    def rdf_type(self):
        return self.rdf_type_db.as_context

    @rdf_type.setter
    def rdf_type(self, val):
        val = URIRefDb.get_or_create_from_ctx(val, self.db)
        if val != self.rdf_type_db:
            self.rdf_type_db = val
            self.applyTypeRules()

    def get_children(self):
        return self.db.query(Idea).join(
            IdeaLink, (IdeaLink.target_id == Idea.id)
            & (IdeaLink.tombstone_date == None)).filter(
            (IdeaLink.source_id == self.id)
            & (Idea.tombstone_date == None)
            ).order_by(IdeaLink.order).all()

    def get_parents(self):
        return self.db.query(Idea).join(
            IdeaLink, (IdeaLink.source_id == Idea.id)
            & (IdeaLink.tombstone_date == None)).filter(
            (IdeaLink.target_id == self.id)
            & (Idea.tombstone_date == None)).all()

    def safe_title(self, user_prefs, localizer=None):
        if self.title:
            entry = self.title.best_lang(user_prefs)
            if entry:
                return entry.value
        # absurd fallback
        text = _("Idea")
        if localizer:
            text = localizer.translate(text)
        return " ".join((text, str(self.id)))

    @property
    def parent_uris(self):
        return [Idea.uri_generic(l.source_id) for l in self.source_links]

    @property
    def children_uris(self):
        return [Idea.uri_generic(l.target_id) for l in self.target_links]

    @property
    def widget_add_post_endpoint(self):
        # Only for api v2
        from pyramid.threadlocal import get_current_request
        from .widgets import Widget
        req = get_current_request() or {}
        ctx = getattr(req, 'context', {})
        if getattr(ctx, 'get_instance_of_class', None):
            # optional optimization
            widget = ctx.get_instance_of_class(Widget)
            if widget:
                if getattr(widget, 'get_add_post_endpoint', None):
                    return {widget.uri(): widget.get_add_post_endpoint(self)}
            else:
                return self.widget_ancestor_endpoints(self)

    def widget_ancestor_endpoints(self, target_idea=None):
        # HACK. Review consequences after test.
        target_idea = target_idea or self
        inherited = dict()
        for p in self.get_parents():
            inherited.update(p.widget_ancestor_endpoints(target_idea))
        inherited.update({
            widget.uri(): widget.get_add_post_endpoint(target_idea)
            for widget in self.widgets
            if getattr(widget, 'get_add_post_endpoint', None)
        })
        return inherited

    def copy(self, tombstone=None, db=None, **kwargs):
        if tombstone is True:
            tombstone = datetime.utcnow()
        kwargs.update(
            tombstone=tombstone,
            hidden=self.hidden,
            creation_date=self.creation_date,
            discussion=self.discussion,
            title=self.title.clone(db=db) if self.title else None,
            synthesis_title=self.synthesis_title.clone(db=db) if self.synthesis_title else None,
            description=self.description.clone(db=db) if self.description else None)

        return super(Idea, self).copy(db=db, **kwargs)

    @classmethod
    def get_ancestors_query_cls(
            cls, target_id=bindparam('root_id', type_=Integer),
            inclusive=True, tombstone_date=None):
        if cls.using_virtuoso:
            if isinstance(target_id, list):
                raise NotImplementedError()
            sql = text(
                """SELECT transitive t_in (1) t_out (2) T_DISTINCT T_NO_CYCLES
                    source_id, target_id FROM idea_idea_link
                    WHERE tombstone_date IS NULL"""
                ).columns(column('source_id'), column('target_id')).alias()
            select_exp = select([sql.c.source_id.label('id')]
                ).select_from(sql).where(sql.c.target_id==target_id)
        else:
            if isinstance(target_id, list):
                root_condition = IdeaLink.target_id.in_(target_id)
            else:
                root_condition = (IdeaLink.target_id == target_id)
            link = select(
                    [IdeaLink.source_id, IdeaLink.target_id]
                ).select_from(
                    IdeaLink
                ).where(
                    (IdeaLink.tombstone_date == tombstone_date) &
                    (root_condition)
                ).cte(recursive=True)
            target_alias = aliased(link)
            sources_alias = aliased(IdeaLink)
            parent_link = sources_alias.target_id == target_alias.c.source_id
            parents = select(
                    [sources_alias.source_id, sources_alias.target_id]
                ).select_from(sources_alias).where(parent_link
                    & (sources_alias.tombstone_date == tombstone_date))
            with_parents = link.union(parents)
            select_exp = select([with_parents.c.source_id.label('id')]
                ).select_from(with_parents)
        if inclusive:
            if isinstance(target_id, int):
                target_id = literal_column(str(target_id), Integer)
            elif isinstance(target_id, list):
                raise NotImplementedError()
                # postgres: select * from unnest(ARRAY[1,6,7]) as id
            else:
                select_exp = select_exp.union(
                    select([target_id.label('id')]))
        return select_exp.alias('ancestors')

    def get_ancestors_query(
            self, inclusive=True, tombstone_date=None, subquery=True):
        select_exp = self.get_ancestors_query_cls(
            self.id, inclusive=inclusive, tombstone_date=tombstone_date)
        if subquery:
            select_exp = self.db.query(select_exp).subquery()
        return select_exp

    def get_all_ancestors(self, id_only=False):
        query = self.get_ancestors_query(
            tombstone_date=self.tombstone_date, subquery=not id_only)
        if id_only:
            return list((id for (id,) in self.db.query(query)))
        else:
            return self.db.query(Idea).filter(Idea.id.in_(query)).all()

    def get_applicable_announcement(self):
        from .announcement import IdeaAnnouncement
        if self.announcement:
            return self.announcement
        aq = self.get_ancestors_query()
        announcements = self.db.query(IdeaAnnouncement
            ).filter(IdeaAnnouncement.idea_id.in_(aq),
                     IdeaAnnouncement.should_propagate_down==True
            ).all()
        # assume order is preserved from aq...
        if announcements:
            return announcements[-1]

    @classmethod
    def get_descendants_query_cls(
            cls, root_idea_id=bindparam('root_idea_id', type_=Integer),
            inclusive=True):
        if cls.using_virtuoso:
            sql = text(
                """SELECT transitive t_in (1) t_out (2) T_DISTINCT T_NO_CYCLES
                    source_id, target_id FROM idea_idea_link
                    WHERE tombstone_date IS NULL"""
                ).columns(column('source_id'), column('target_id')).alias()
            select_exp = select([sql.c.target_id.label('id')]
                ).select_from(sql).where(sql.c.source_id==root_idea_id)
        else:
            link = select(
                    [IdeaLink.source_id, IdeaLink.target_id]
                ).select_from(
                    IdeaLink
                ).where(
                    (IdeaLink.tombstone_date == None) &
                    (IdeaLink.source_id == root_idea_id)
                ).cte(recursive=True)
            source_alias = aliased(link)
            targets_alias = aliased(IdeaLink)
            parent_link = targets_alias.source_id == source_alias.c.target_id
            children = select(
                    [targets_alias.source_id, targets_alias.target_id]
                ).select_from(targets_alias).where(parent_link
                    & (targets_alias.tombstone_date == None))
            with_children = link.union(children)
            select_exp = select([with_children.c.target_id.label('id')]
                ).select_from(with_children)
        if inclusive:
            if isinstance(root_idea_id, int):
                root_idea_id = literal_column(str(root_idea_id), Integer)
            select_exp = select_exp.union(
                select([root_idea_id.label('id')]))
        return select_exp.alias('descendants')

    def get_descendants_query(
            self, inclusive=True, subquery=True):
        select_exp = self.get_descendants_query_cls(self.id, inclusive=inclusive)
        if subquery:
            select_exp = self.db.query(select_exp).subquery()
        return select_exp

    def get_all_descendants(self, id_only=False, inclusive=True):
        query = self.get_descendants_query(
            inclusive=inclusive, subquery=not id_only)
        if id_only:
            return list((id for (id,) in self.db.query(query)))
        else:
            return self.db.query(Idea).filter(Idea.id.in_(query)).all()

    def get_order_from_first_parent(self):
        return self.source_links[0].order if self.source_links else None

    def get_order_from_first_parent_ts(self):
        return self.source_links_ts[0].order if self.source_links_ts else None

    def get_first_parent_uri(self):
        data = self.get_discussion_data(self.discussion_id, False)
        if data is not None and self.id in data.parent_dict:
            return Idea.uri_generic(data.parent_dict[self.id])
        for link in self.source_links:
            return Idea.uri_generic(link.source_id)

    def get_first_parent_uri_ts(self):
        return Idea.uri_generic(
            self.source_links_ts[0].source_id
        ) if self.source_links_ts else None

    @classmethod
    def get_related_posts_query_c(
            cls, discussion_id, root_idea_id, partial=False,
            include_deleted=False):
        from .generic import Content
        counters = cls.prepare_counters(discussion_id)
        if partial:
            return counters.paths[root_idea_id].as_clause_base(
                cls.default_db(), discussion_id, include_deleted=include_deleted)
        else:
            return counters.paths[root_idea_id].as_clause(
                cls.default_db(), discussion_id, counters.user_id, Content,
                include_deleted=include_deleted)

    @classmethod
    def get_discussion_data(cls, discussion_id, create=True):
        from pyramid.threadlocal import get_current_request
        from .path_utils import DiscussionGlobalData
        from pyramid.security import authenticated_userid
        req = get_current_request()
        discussion_data = None
        if req:
            discussion_data = getattr(req, "discussion_data", None)
        if create and not discussion_data:
            discussion_data = DiscussionGlobalData(
                cls.default_db(), discussion_id,
                authenticated_userid(req) if req else None)
            if req:
                req.discussion_data = discussion_data
        return discussion_data

    @classmethod
    def prepare_counters(cls, discussion_id, calc_all=False):
        discussion_data = cls.get_discussion_data(discussion_id)
        return discussion_data.post_path_counter(
            discussion_data.user_id, calc_all)

    def get_related_posts_query(self, partial=False, include_deleted=False):
        return self.get_related_posts_query_c(
            self.discussion_id, self.id, partial,
            include_deleted=include_deleted)

    @classmethod
    def _get_orphan_posts_statement(
            cls, discussion_id, get_read_status=False, content_alias=None,
            include_deleted=False):
        """ Requires discussion_id bind parameters
        Excludes synthesis posts """
        counters = cls.prepare_counters(discussion_id)
        return counters.orphan_clause(
            counters.user_id if get_read_status else None,
            content_alias, include_deleted=include_deleted)

    @property
    def num_posts(self):
        counters = self.prepare_counters(self.discussion_id)
        return counters.get_counts(self.id)[0]

    @property
    def num_contributors(self):
        counters = self.prepare_counters(self.discussion_id)
        return counters.get_counts(self.id)[1]

    @property
    def num_read_posts(self):
        counters = self.prepare_counters(self.discussion_id)
        return counters.get_counts(self.id)[2]

    @property
    def num_total_and_read_posts(self):
        counters = self.prepare_counters(self.discussion_id)
        return counters.get_counts(self.id)

    def prefetch_descendants(self):
        # TODO maparent: descendants only. Let's just prefetch all ideas.
        ideas = self.db.query(Idea).filter_by(
            discussion_id=self.discussion_id, tombstone_date=None).all()
        ideas_by_id = {idea.id: idea for idea in ideas}
        children_id_dict = self.children_dict(self.discussion_id)
        return {
            id: [ideas_by_id[child_id] for child_id in child_ids]
            for (id, child_ids) in children_id_dict.items()
        }

    def visit_ideas_depth_first(self, idea_visitor):
        children_dict = self.prefetch_descendants()
        return self._visit_ideas_depth_first(idea_visitor, set(), 0, None, children_dict)

    def _visit_ideas_depth_first(
            self, idea_visitor, visited, level, prev_result, children_dict):
        if self in visited:
            # not necessary in a tree, but let's start to think graph.
            return False
        result = idea_visitor.visit_idea(self, level, prev_result)
        visited.add(self)
        child_results = []
        if result is not IdeaVisitor.CUT_VISIT:
            for child in children_dict.get(self.id, ()):
                r = child._visit_ideas_depth_first(
                    idea_visitor, visited, level+1, result, children_dict)
                if r:
                    child_results.append((child, r))
        return idea_visitor.end_visit(self, level, result, child_results)

    @classmethod
    def children_dict(cls, discussion_id):
        # We do not want a subclass
        cls = [c for c in cls.mro() if c.__name__=="Idea"][0]
        source = aliased(cls, name="source")
        target = aliased(cls, name="target")
        link_info = list(cls.default_db.query(
            IdeaLink.target_id, IdeaLink.source_id
            ).join(source, source.id == IdeaLink.source_id
            ).join(target, target.id == IdeaLink.target_id
            ).filter(
            source.discussion_id == discussion_id,
            IdeaLink.tombstone_date == None,
            source.tombstone_date == None,
            target.tombstone_date == None,
            target.discussion_id == discussion_id
            ).order_by(IdeaLink.order))
        if not link_info:
            (root_id,) = cls.default_db.query(
                RootIdea.id).filter_by(discussion_id=discussion_id).first()
            return {None: (root_id,), root_id: ()}
        child_nodes = {child for (child, parent) in link_info}
        children_of = defaultdict(list)
        for (child, parent) in link_info:
            children_of[parent].append(child)
        root = set(children_of.keys()) - child_nodes
        assert len(root) == 1
        children_of[None] = [root.pop()]
        return children_of

    @classmethod
    def visit_idea_ids_depth_first(
            cls, idea_visitor, discussion_id, children_dict=None):
        # Lightweight descent
        if children_dict is None:
            children_dict = cls.children_dict(discussion_id)
        root_id = children_dict[None][0]
        return cls._visit_idea_ids_depth_first(
            root_id, idea_visitor, children_dict, set(), 0, None)

    @classmethod
    def _visit_idea_ids_depth_first(
            cls, idea_id, idea_visitor, children_dict, visited,
            level, prev_result):
        if idea_id in visited:
            # not necessary in a tree, but let's start to think graph.
            return False
        result = idea_visitor.visit_idea(idea_id, level, prev_result)
        visited.add(idea_id)
        child_results = []
        if result is not IdeaVisitor.CUT_VISIT:
            for child_id in children_dict[idea_id]:
                r = cls._visit_idea_ids_depth_first(
                    child_id, idea_visitor, children_dict, visited, level+1, result)
                if r:
                    child_results.append((child_id, r))
        return idea_visitor.end_visit(idea_id, level, result, child_results)

    def visit_ideas_breadth_first(self, idea_visitor):
        self.prefetch_descendants()
        result = idea_visitor.visit_idea(self, 0, None)
        visited = {self}
        if result is not IdeaVisitor.CUT_VISIT:
            return self._visit_ideas_breadth_first(
                idea_visitor, visited, 1, result)

    def _visit_ideas_breadth_first(
            self, idea_visitor, visited, level, prev_result):
        children = []
        result = True
        child_results = []
        for child in self.get_children():
            if child in visited:
                continue
            result = idea_visitor.visit_idea(child, level, prev_result)
            visited.add(child)
            if result != IdeaVisitor.CUT_VISIT:
                children.append(child)
                if result:
                    child_results.append((child, r))
        for child in children:
            child._visit_ideas_breadth_first(
                idea_visitor, visited, level+1, result)
        return idea_visitor.end_visit(self, level, prev_result, child_results)

    def most_common_words(self, lang=None, num=8):
        if lang:
            langs = (lang,)
        else:
            langs = self.discussion.discussion_locales
        word_counter = WordCountVisitor(langs)
        self.visit_ideas_depth_first(word_counter)
        return word_counter.best(num)

    @property
    def most_common_words_prop(self):
        return self.most_common_words()

    def get_siblings_of_type(self, cls):
        # TODO: optimize
        siblings = set(chain(*(p.children for p in self.get_parents())))
        if siblings:
            siblings.remove(self)
        return [c for c in siblings if isinstance(c, cls)]

    def get_synthesis_contributors(self, id_only=True):
        # author of important extracts
        from .idea_content_link import Extract
        from .auth import AgentProfile
        from .post import Post
        from .generic import Content
        from sqlalchemy.sql.functions import count
        subquery = self.get_descendants_query()
        query = self.db.query(
            Post.creator_id
            ).join(Extract
            ).join(subquery, Extract.idea_id == subquery.c.id
            ).filter(Extract.important == True
            ).group_by(Post.creator_id
            ).order_by(count(Extract.id).desc())
        if id_only:
            return [AgentProfile.uri_generic(a) for (a,) in query]
        else:
            ids = [x for (x,) in query]
            if not ids:
                return []
            agents = {a.id: a for a in self.db.query(AgentProfile).filter(
                AgentProfile.id.in_(ids))}
            return [agents[id] for id in ids]

    def get_contributors(self):
        from .generic import Content
        from .post import Post
        from sqlalchemy.sql.functions import count
        related = self.get_related_posts_query(True)
        content = with_polymorphic(
            Content, [], Content.__table__,
            aliased=False, flat=True)
        post = with_polymorphic(
            Post, [], Post.__table__,
            aliased=False, flat=True)
        query = self.db.query(post.creator_id
            ).join(content, post.id == content.id
            ).join(related, content.id == related.c.post_id
            ).filter(content.hidden == False,
                content.discussion_id == self.discussion_id
            ).group_by(
                post.creator_id
            ).order_by(
                count(post.id.distinct()).desc())

        return ['local:Agent/' + str(i) for (i,) in query]

    def applyTypeRules(self):
        from ..semantic.inference import get_inference_store
        ontology = get_inference_store()
        typology = self.discussion.preferences['idea_typology'] or {}
        rules = typology.get('ideas', {}).get(self.rdf_type, {}).get('rules', {})
        for child_link in self.target_links:
            link_type = child_link.rdf_type
            child = child_link.target
            child_type = child.rdf_type
            if child_type != 'GenericIdeaNode':
                child_types = (
                    set(ontology.getSuperClassesCtx(child_type)) -
                    set(ontology.getSuperClassesCtx('GenericIdeaNode')))
            else:
                child_types = set((child_type,))
            if link_type != 'InclusionRelation':
                link_types = (
                    set(ontology.getSuperClassesCtx(link_type)) -
                    set(ontology.getSuperClassesCtx('InclusionRelation')))
            else:
                link_types = set((link_type,))
            if link_type not in rules:
                # TODO: no real guarantee of mro ordering in that function
                if link_type not in rules:
                    for supertype in link_types:
                        if supertype in rules:
                            break
                    else:
                        supertype = 'InclusionRelation'
                    child_link.rdf_type = link_type = supertype
            node_rules = rules.get(link_type, ())
            if child_type not in node_rules:
                # Ideally keep child type stable. In order:
                # 0: Supertype of link and same child_type
                # 1: Any link with same child_type
                # 2: Original link with child supertype
                # 3: Supertype of link with child supertype
                # 4: Original link with generic child type
                potential_link_types = []
                for r_link_type, r_child_types in rules.items():
                    r_child_types = set(r_child_types)
                    if child_type in r_child_types:
                        potential_link_types.append((
                            0 if r_link_type in link_types else 1,
                            r_link_type, child_type))
                    else:
                        inter = child_types.intersection(r_child_types)
                        if inter:
                            potential_link_types.append((
                                2 if r_link_type == link_type else 3,
                                r_link_type, inter.pop()))
                if 'GenericIdeaNode' in node_rules:
                    potential_link_types.append((4, link_type, 'GenericIdeaNode'))
                else:
                    potential_link_types.append((5, 'InclusionRelation', 'GenericIdeaNode'))
                potential_link_types.sort()
                _, child_link.rdf_type, new_child_type = potential_link_types[0]
                if new_child_type != child_type:
                    child.rdf_type = new_child_type
                    child.applyTypeRules()

    def get_discussion_id(self):
        return self.discussion_id or self.discussion.id

    def get_definition_preview(self):
        body = self.definition.strip()
        target_len = 120
        shortened = False
        html_len = 2 * target_len
        while True:
            text = sanitize_text(body[:html_len])
            if html_len >= len(body) or len(text) > target_len:
                shortened = html_len < len(body)
                body = text
                break
            html_len += target_len
        if len(body) > target_len:
            body = body[:target_len].rsplit(' ', 1)[0].rstrip() + ' '
        elif shortened:
            body += ' '
        return body

    def get_url(self):
        from assembl.lib.frontend_urls import FrontendUrls
        frontendUrls = FrontendUrls(self.discussion)
        return frontendUrls.get_idea_url(self)

    @classmethod
    def get_discussion_conditions(cls, discussion_id, alias_maker=None):
        return (cls.discussion_id == discussion_id,)

    def send_to_changes(self, connection=None, operation=CrudOperation.UPDATE,
                        discussion_id=None, view_def="changes"):
        """invoke the modelWatcher on creation"""
        connection = connection or self.db.connection()
        if self.is_tombstone:
            self.tombstone().send_to_changes(
                connection, CrudOperation.DELETE, discussion_id, view_def)
        else:
            super(Idea, self).send_to_changes(
                connection, operation, discussion_id, view_def)
        watcher = get_model_watcher()
        if operation == CrudOperation.UPDATE:
            watcher.processIdeaModified(self.id, 0)  # no versions yet.
        elif operation == CrudOperation.DELETE:
            watcher.processIdeaDeleted(self.id)
        elif operation == CrudOperation.CREATE:
            watcher.processIdeaCreated(self.id)

    @as_native_str()
    def __repr__(self):
        r = super(Idea, self).__repr__()
        title = self.short_title or ""
        return r[:-1] + title + ">"

    @classmethod
    def invalidate_ideas(cls, discussion_id, post_id):
        raise NotImplementedError()

    @classmethod
    def get_idea_ids_showing_post(cls, post_id):
        "Given a post, give the ID of the ideas that show this message"
        from sqlalchemy.sql.functions import func
        from .idea_content_link import IdeaContentPositiveLink
        from .post import Post
        (ancestry, discussion_id, idea_link_ids)  = cls.default_db.query(
            Post.ancestry, Post.discussion_id,
            func.idea_content_links_above_post(Post.id)
            ).filter(Post.id==post_id).first()
        post_path = "%s%d," % (ancestry, post_id)
        if not idea_link_ids:
            return []
        idea_link_ids = [int(id) for id in idea_link_ids.split(',') if id]
        # This could be combined with previous in postgres.
        root_ideas = cls.default_db.query(
                IdeaContentPositiveLink.idea_id.distinct()
            ).filter(
                IdeaContentPositiveLink.idea_id != None,
                IdeaContentPositiveLink.id.in_(idea_link_ids)).all()
        if not root_ideas:
            return []
        root_ideas = [x for (x,) in root_ideas]
        discussion_data = cls.get_discussion_data(discussion_id)
        counter = cls.prepare_counters(discussion_id)
        idea_contains = {}
        for root_idea_id in root_ideas:
            for idea_id in discussion_data.idea_ancestry(root_idea_id):
                if idea_id in idea_contains:
                    break
                idea_contains[idea_id] = counter.paths[idea_id].includes_post(post_path)
        ideas = [id for (id, incl) in idea_contains.items() if incl]
        return ideas

    @classmethod
    def idea_read_counts(cls, discussion_id, post_id, user_id):
        """Given a post and a user, give the total and read count
            of posts for each affected idea"""
        idea_ids = cls.get_idea_ids_showing_post(post_id)
        if not idea_ids:
            return []
        ideas = cls.default_db.query(cls).filter(cls.id.in_(idea_ids))
        return [(idea.id, idea.num_read_posts)
                for idea in ideas]

    def get_widget_creation_urls(self):
        from .widgets import GeneratedIdeaWidgetLink
        return [wl.context_url for wl in self.widget_links
                if isinstance(wl, GeneratedIdeaWidgetLink)]

    # def get_notifications(self):
    #     # Dead code?
    #     from .widgets import BaseIdeaWidgetLink
    #     for widget_link in self.widget_links:
    #         if not isinstance(self, BaseIdeaWidgetLink):
    #             continue
    #         for n in widget_link.widget.has_notification():
    #             yield n

    @classmethod
    def get_all_idea_links(cls, discussion_id):
        target = aliased(cls)
        source = aliased(cls)
        return cls.default_db.query(
            IdeaLink).join(
            source, source.id == IdeaLink.source_id).join(
            target, target.id == IdeaLink.target_id).filter(
            target.discussion_id == discussion_id).filter(
            source.discussion_id == discussion_id).filter(
            IdeaLink.tombstone_date == None).all()

    @classmethod
    def extra_collections(cls):
        from .widgets import Widget
        from .idea_content_link import (
            IdeaRelatedPostLink, IdeaContentWidgetLink)
        from .generic import Content
        from .post import Post, WidgetPost
        from ..views.traversal import NsDictCollection

        class ChildIdeaCollectionDefinition(AbstractCollectionDefinition):
            def __init__(self, cls):
                super(ChildIdeaCollectionDefinition, self).__init__(
                    cls, 'children', Idea)

            def decorate_query(self, query, owner_alias, last_alias, parent_instance, ctx):
                parent = owner_alias
                children = last_alias
                return query.join(
                    IdeaLink, IdeaLink.target_id == children.id).join(
                    parent, IdeaLink.source_id == parent.id).filter(
                    IdeaLink.source_id == parent_instance.id,
                    IdeaLink.tombstone_date == None,
                    children.tombstone_date == None)

            def contains(self, parent_instance, instance):
                return instance.db.query(
                    IdeaLink).filter_by(
                    source=parent_instance, target=instance
                    ).count() > 0

        @collection_creation_side_effects.register(
            inst_ctx=Idea, ctx='Idea.children')
        def add_child_link(inst_ctx, ctx):
            yield InstanceContext(
                inst_ctx['target_links'],
                IdeaLink(
                    source=ctx.parent_instance, target=inst_ctx._instance))

        class LinkedPostCollectionDefinition(AbstractCollectionDefinition):
            # used by inspiration widget
            def __init__(self, cls):
                super(LinkedPostCollectionDefinition, self).__init__(
                    cls, 'linkedposts', Content)

            def decorate_query(self, query, owner_alias, last_alias, parent_instance, ctx):
                return query.join(IdeaRelatedPostLink, owner_alias)

            def contains(self, parent_instance, instance):
                return instance.db.query(
                    IdeaRelatedPostLink).filter_by(
                    content=instance, idea=parent_instance
                    ).count() > 0

        @collection_creation_side_effects.register(
            inst_ctx=Post, ctx='Idea.linkedposts')
        def add_related_post_link(inst_ctx, ctx):
            post = inst_ctx._instance
            idea = ctx.parent_instance
            link = IdeaRelatedPostLink(
                content=post, idea=idea,
                creator=post.creator)
            yield InstanceContext(
                inst_ctx['idea_links_of_content'], link)

        @collection_creation_side_effects.register(
            inst_ctx=WidgetPost, ctx='Idea.linkedposts')
        def add_youtube_attachment(inst_ctx, ctx):
            from .attachment import Document, PostAttachment
            for subctx in add_related_post_link(inst_ctx, ctx):
                yield subctx
            post = inst_ctx._instance
            insp_url = post.metadata_json.get('inspiration_url', '')
            if insp_url.startswith("https://www.youtube.com/"):
                # TODO: detect all video/image inspirations.
                # Handle duplicates in docs!
                # Check whether we already have such an attachment?
                doc = Document(
                    discussion=post.discussion,
                    uri_id=insp_url)
                doc = doc.handle_duplication()
                attachment_ctx = InstanceContext(
                    inst_ctx['attachments'],
                    PostAttachment(
                        discussion=post.discussion,
                        creator=post.creator,
                        document=doc,
                        attachmentPurpose='EMBED_ATTACHMENT',
                        post=post))
                yield attachment_ctx
                yield InstanceContext(
                    attachment_ctx['document'], doc)

        class WidgetPostCollectionDefinition(AbstractCollectionDefinition):
            # used by creativity widget
            def __init__(self, cls):
                super(WidgetPostCollectionDefinition, self).__init__(
                    cls, 'widgetposts', Content)

            def decorate_query(self, query, owner_alias, last_alias, parent_instance, ctx):
                from .post import IdeaProposalPost
                idea = owner_alias
                query = query.join(IdeaContentWidgetLink).join(
                    idea,
                    IdeaContentWidgetLink.idea_id == parent_instance.id)
                if Content in chain(*(
                        mapper.entities for mapper in query._entities)):
                    query = query.options(
                        contains_eager(Content.widget_idea_links))
                        # contains_eager(Content.extracts) seems to slow things down instead
                # Filter out idea proposal posts
                query = query.filter(last_alias.type.notin_(
                    IdeaProposalPost.polymorphic_identities()))
                return query

            def contains(self, parent_instance, instance):
                return instance.db.query(
                    IdeaContentWidgetLink).filter_by(
                    content=instance, idea=parent_instance
                    ).count() > 0

        @collection_creation_side_effects.register(
            inst_ctx=Post, ctx='Idea.widgetposts')
        def add_content_widget_link(inst_ctx, ctx):
            obj = inst_ctx._instance
            if ctx.parent_instance.proposed_in_post:
                obj.set_parent(ctx.parent_instance.proposed_in_post)
            obj.hidden = True
            yield InstanceContext(
                inst_ctx['idea_links_of_content'],
                IdeaContentWidgetLink(
                    content=obj, idea=ctx.parent_instance,
                    creator=obj.creator))

        class ActiveShowingWidgetsCollection(RelationCollectionDefinition):
            def __init__(self, cls):
                super(ActiveShowingWidgetsCollection, self).__init__(
                    cls, cls.active_showing_widget_links)
            def decorate_query(self, query, owner_alias, last_alias, parent_instance, ctx):
                from .widgets import IdeaShowingWidgetLink
                idea = owner_alias
                widget_idea_link = last_alias
                query = query.join(
                    idea, widget_idea_link.idea).join(
                    Widget, widget_idea_link.widget).filter(
                    Widget.test_active(),
                    widget_idea_link.type.in_(
                        IdeaShowingWidgetLink.polymorphic_identities()),
                    idea.id == parent_instance.id)
                return query

        return (ChildIdeaCollectionDefinition(cls),
                LinkedPostCollectionDefinition(cls),
                WidgetPostCollectionDefinition(cls),
                NsDictCollection(cls),
                ActiveShowingWidgetsCollection(cls))

    def widget_link_signatures(self):
        from .widgets import Widget
        return [
            {'widget': Widget.uri_generic(l.widget_id),
             '@type': l.external_typename()}
            for l in self.widget_links]

    def active_widget_uris(self):
        from .widgets import Widget
        return [Widget.uri_generic(l.widget_id)
                for l in self.active_showing_widget_links]

    crud_permissions = CrudPermissions(
        P_ADD_IDEA, P_READ, P_EDIT_IDEA, P_ADMIN_DISC, P_ADMIN_DISC,
        P_ADMIN_DISC)

LangString.setup_ownership_load_event(Idea,
    ['title', 'description', 'synthesis_title'])


class RootIdea(Idea):
    """
    The root idea.  It represents the discussion.

    It has implicit links to all content and posts in the discussion.
    """
    root_for_discussion = relationship(
        Discussion,
        backref=backref('root_idea', uselist=False),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'root_idea',
    }


    def __init__(self, *args, **kwargs):
        kwargs['rdf_type_id'] = 3
        super(RootIdea, self).__init__(*args, **kwargs)

    @property
    def num_posts(self):
        """ In the root idea, num_posts is the count of all non-deleted mesages in the discussion """
        from .post import Post
        result = self.db.query(Post).filter(
            Post.discussion_id == self.discussion_id,
            Post.hidden==False,
            Post.tombstone_condition()
        ).count()
        return int(result)

    @property
    def num_read_posts(self):
        """ In the root idea, num_posts is the count of all non-deleted read mesages in the discussion """
        from .post import Post
        from .action import ViewPost
        discussion_data = self.get_discussion_data(self.discussion_id)
        result = self.db.query(Post).filter(
            Post.discussion_id == self.discussion_id,
            Post.hidden==False,
            Post.tombstone_condition()
        ).join(
            ViewPost,
            (ViewPost.post_id == Post.id)
            & (ViewPost.tombstone_date == None)
            & (ViewPost.actor_id == discussion_data.user_id)
        ).count()
        return int(result)

    @property
    def num_contributors(self):
        """ In the root idea, num_posts is the count of contributors to
        all non-deleted mesages in the discussion """
        from .post import Post
        result = self.db.query(Post.creator_id).filter(
            Post.discussion_id == self.discussion_id,
            Post.hidden==False,
            Post.tombstone_condition()
        ).distinct().count()
        return int(result)

    @property
    def num_total_and_read_posts(self):
        return (self.num_posts, self.num_contributors, self.num_read_posts)

    @property
    def num_orphan_posts(self):
        "The number of posts unrelated to any idea in the current discussion"
        counters = self.prepare_counters(self.discussion_id)
        return counters.get_orphan_counts()[0]

    @property
    def num_synthesis_posts(self):
        """ In the root idea, this is the count of all published and non-deleted SynthesisPost of the discussion """
        return self.discussion.get_all_syntheses_query(False).count()

    def discussion_topic(self):
        return self.discussion.topic

    crud_permissions = CrudPermissions(P_ADMIN_DISC)


class IdeaLink(HistoryMixinWithOrigin, DiscussionBoundBase):
    """
    A generic link between two ideas

    If a parent-child relation, the parent is the source, the child the target.
    Note: it's reversed in the RDF model.
    """
    __tablename__ = 'idea_idea_link'
    __external_typename = "DirectedIdeaRelation"
    rdf_class = IDEA.DirectedIdeaRelation
    rdf_type_id = Column(
            Integer, ForeignKey('uriref.id'),
            server_default=str(URIRefDb.index_of(IDEA.InclusionRelation)))
    source_id = Column(
        Integer, ForeignKey(
            'idea.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False, index=True)
        #info={'rdf': QuadMapPatternS(None, IDEA.target_idea)})
    target_id = Column(Integer, ForeignKey(
        'idea.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False, index=True)
    source = relationship(
        'Idea',
        primaryjoin="and_(Idea.id==IdeaLink.source_id, "
                    "Idea.tombstone_date == None)",
        backref=backref(
            'target_links',
            primaryjoin="and_(Idea.id==IdeaLink.source_id, "
                        "IdeaLink.tombstone_date == None)",
            cascade="all, delete-orphan"),
        foreign_keys=(source_id))
    target = relationship(
        'Idea',
        primaryjoin="and_(Idea.id==IdeaLink.target_id, "
                    "Idea.tombstone_date == None)",
        backref=backref(
            'source_links',
            primaryjoin="and_(Idea.id==IdeaLink.target_id, "
                        "IdeaLink.tombstone_date == None)",
            cascade="all, delete-orphan"),
        foreign_keys=(target_id))
    source_ts = relationship(
        'Idea',
        backref=backref('target_links_ts', cascade="all, delete-orphan"),
        foreign_keys=(source_id))
    target_ts = relationship(
        'Idea',
        backref=backref('source_links_ts', cascade="all, delete-orphan"),
        foreign_keys=(target_id))
    order = Column(
        Float, nullable=False, default=0.0,
        info={'rdf': QuadMapPatternS(None, ASSEMBL.link_order)})

    rdf_type_db = relationship(URIRefDb)

    @property
    def rdf_type_url(self):
        return self.rdf_type_db.val

    @rdf_type_url.setter
    def rdf_type_url(self, val):
        self.rdf_type_db = URIRefDb.get_or_create(val, self.db)

    @property
    def rdf_type_curie(self):
        return self.rdf_type_db.as_curie

    @rdf_type_curie.setter
    def rdf_type_curie(self, val):
        self.rdf_type_db = URIRefDb.get_or_create_from_curie(val, self.db)

    @property
    def rdf_type(self):
        return self.rdf_type_db.as_context

    @rdf_type.setter
    def rdf_type(self, val):
        self.rdf_type_db = URIRefDb.get_or_create_from_ctx(val, self.db)

    def populate_from_context(self, context):
        if not(self.source or self.source_ts or self.source_id):
            self.source = context.get_instance_of_class(Idea)
        super(IdeaLink, self).populate_from_context(context)

    @classmethod
    def base_conditions(cls, alias=None, alias_maker=None):
        if alias_maker is None:
            idea_link = alias or cls
            source_idea = Idea
        else:
            idea_link = alias or alias_maker.alias_from_class(cls)
            source_idea = alias_maker.alias_from_relns(idea_link.source)

        # Assume tombstone status of target is similar to source, for now.
        return ((idea_link.tombstone_date == None),
                (idea_link.source_id == source_idea.id),
                (source_idea.tombstone_date == None))

    @classmethod
    def special_quad_patterns(cls, alias_maker, discussion_id):
        idea_link = alias_maker.alias_from_class(cls)
        target_alias = alias_maker.alias_from_relns(cls.target)
        source_alias = alias_maker.alias_from_relns(cls.source)
        # Assume tombstone status of target is similar to source, for now.
        conditions = [(idea_link.target_id == target_alias.id),
                      (target_alias.tombstone_date == None)]
        if discussion_id:
            conditions.append((target_alias.discussion_id == discussion_id))
        return [
            QuadMapPatternS(
                Idea.iri_class().apply(idea_link.source_id),
                IDEA.includes,
                Idea.iri_class().apply(idea_link.target_id),
                conditions=conditions,
                name=QUADNAMES.idea_inclusion_reln),
            QuadMapPatternS(
                cls.iri_class().apply(idea_link.id),
                IDEA.source_idea,  # Note that RDF is inverted
                Idea.iri_class().apply(idea_link.target_id),
                conditions=conditions,
                name=QUADNAMES.col_pattern_IdeaLink_target_id
                #exclude_base_condition=True
                ),
            QuadMapPatternS(
                cls.iri_class().apply(idea_link.id),
                IDEA.target_idea,
                Idea.iri_class().apply(idea_link.source_id),
                name=QUADNAMES.col_pattern_IdeaLink_source_id
                ),
            QuadMapPatternS(
                None, RDF.type, IriClass(VirtRDF.QNAME_ID).apply(IdeaLink.rdf_type_db.val),
                name=QUADNAMES.class_IdeaLink_class),
        ]

    def copy(self, tombstone=None, db=None, **kwargs):
        kwargs.update(
            tombstone=tombstone,
            order=self.order,
            creation_date=self.creation_date,
            source_id=self.source_id,
            target_id=self.target_id)
        return super(IdeaLink, self).copy(db=db, **kwargs)

    def get_discussion_id(self):
        source = self.source_ts or self.source or Idea.get(self.source_id)
        return source.get_discussion_id()

    def send_to_changes(self, connection=None, operation=CrudOperation.UPDATE,
                        discussion_id=None, view_def="changes"):
        connection = connection or self.db.connection()
        if self.is_tombstone:
            self.tombstone().send_to_changes(
                connection, CrudOperation.DELETE, discussion_id, view_def)
        else:
            super(IdeaLink, self).send_to_changes(
                connection, operation, discussion_id, view_def)

    @classmethod
    def get_discussion_conditions(cls, discussion_id, alias_maker=None):
        if alias_maker is None:
            idea_link = cls
            source_idea = Idea
        else:
            idea_link = alias_maker.alias_from_class(cls)
            source_idea = alias_maker.alias_from_relns(idea_link.source)
        return ((idea_link.source_id == source_idea.id),
                (source_idea.discussion_id == discussion_id))

    crud_permissions = CrudPermissions(
        P_ADD_IDEA, P_READ, P_EDIT_IDEA, P_EDIT_IDEA, P_EDIT_IDEA, P_EDIT_IDEA)

    # discussion = relationship(
    #     Discussion, viewonly=True, uselist=False, backref="idea_links",
    #     secondary=Idea.__table__, primaryjoin=(source_id == Idea.id),
    #     info={'rdf': QuadMapPatternS(None, ASSEMBL.in_conversation)})


    discussion = relationship(
        Discussion,
        viewonly=True,
        uselist=False,
        secondary=Idea.__table__,
        primaryjoin=(source_id == Idea.id),
        # secondaryjoin=(Idea.discussion_id == Discussion.id),
        backref=backref(
            'idea_links',
            primaryjoin=(Idea.discussion_id == Discussion.id),
            secondaryjoin="""and_(IdeaLink.source_id==Idea.id,
                             Idea.tombstone_date == None,
                             IdeaLink.tombstone_date == None)"""),
        info={'rdf': QuadMapPatternS(None, ASSEMBL.in_conversation)}
    )

    discussion_ts = relationship(
        Discussion,
        viewonly=True,
        uselist=False,
        secondary=Idea.__table__,
        primaryjoin=(source_id == Idea.id),
        backref='idea_links_ts',
        info={'rdf': QuadMapPatternS(None, ASSEMBL.in_conversation)}
    )


_it = Idea.__table__
_ilt = IdeaLink.__table__
Idea.num_children = column_property(
    select([func.count(_ilt.c.id)]).where(
        (_ilt.c.source_id == _it.c.id)
        & (_ilt.c.tombstone_date == None)
        & (_it.c.tombstone_date == None)
        ).correlate_except(_ilt),
    deferred=True)

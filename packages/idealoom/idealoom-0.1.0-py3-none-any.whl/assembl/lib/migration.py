"""Basic infrastructure for alembic migration"""
from __future__ import absolute_import

import sys

from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory

from ..lib.sqla import (
    get_metadata, get_session_maker, mark_changed)
from ..lib.text_search import update_indices


def bootstrap_db(config_uri=None, with_migration=True):
    """Bring a blank database to a functional state."""

    db = get_session_maker()

    if with_migration:
        context = MigrationContext.configure(db().connection())
        db_version = context.get_current_revision()

        if db_version:
            sys.stderr.write('Database already initialized. Bailing out.\n')
            sys.exit(0)

        config = Config(config_uri)
        script_dir = ScriptDirectory.from_config(config)
        heads = script_dir.get_heads()

        if len(heads) > 1:
            sys.stderr.write('Error: migration scripts have more than one '
                             'head.\nPlease resolve the situation before '
                             'attempting to bootstrap the database.\n')
            sys.exit(2)

    import assembl.models
    get_metadata().create_all(db().connection())

    # Clean up the sccoped session to allow a later app instantiation.
    if with_migration and heads:
        context = MigrationContext.configure(db().connection())
        context._ensure_version_table()
        # The latter step seems optional?
        # I am unclear as to why we'd migrate after creating tables
        # on a clean database.
        context.stamp(script_dir, heads[0])
    return db


def bootstrap_db_data(db, mark=True):
    from assembl.lib.config import get
    if get('in_alembic'):
        return
    # import after session to delay loading of BaseOps
    from assembl.models import (
        Permission, Role, IdentityProvider, LocaleLabel, URIRefDb)
    from assembl.lib.database_functions import ensure_functions
    session = db()
    for cls in (Permission, Role, IdentityProvider, LocaleLabel, URIRefDb):
        cls.populate_db(session)
    ensure_functions(session)
    mark |= update_indices(session)
    if mark:
        mark_changed(session)


def ensure_db_version(config_uri, session_maker):
    """Exit if database is not up-to-date."""
    config = Config(config_uri)
    script_dir = ScriptDirectory.from_config(config)
    heads = script_dir.get_heads()

    if len(heads) > 1:
        sys.stderr.write('Error: migration scripts have more than one head.\n'
                         'Please resolve the situation before attempting to '
                         'start the application.\n')
        sys.exit(2)
    else:
        repo_version = heads[0] if heads else None

    context = MigrationContext.configure(session_maker()().connect())
    db_version = context.get_current_revision()

    if not db_version:
        sys.stderr.write('Database not initialized.\n'
                         'Try this: "idealoom-db-manage %s bootstrap".\n'
                         % config_uri)
        sys.exit(2)

    if db_version != repo_version:
        sys.stderr.write('Stopping: DB version (%s) not up-to-date (%s).\n'
                         % (db_version, repo_version))
        sys.stderr.write('Try this: "idealoom-db-manage %s upgrade head".\n'
                         % config_uri)
        sys.exit(2)


def is_migration_script():
    """Determine weather the current process is a migration script."""
    return 'alembic' in sys.argv[0] or 'idealoom-db-manage' in sys.argv[0]


def delete_boolean_constraint(db, table, column):
    # Virtuoso is annoying with schema migration.
    # Dropping the column does not delete the constraint. WHY????
    # Also, CHECK constraints are generally unnamed.
    from assembl.lib import config
    from assembl.sqla import using_virtuoso
    if not using_virtuoso():
        return
    username = config.get('db_user')
    schema = config.get('db_schema')
    constraints = list(db.execute("select c_text, c_mode from db.dba.sys_constraints where c_table = '%s.%s.%s'" % (
        schema, username, table)))
    treated = set()
    for constraint_name, constraint_code in constraints:
        if constraint_name in treated:
            continue
        # column name substring would be annoying...
        if column in constraint_code:
            db.execute('alter table "%s"."%s"."%s" drop constraint "%s"' % (
                schema, username, table, constraint_name))
            treated.add(constraint_name)


def includeme(config):
    """Initialize Alembic-related stuff at app start-up time."""
    skip_migration = config.registry.settings.get('app.skip_migration')
    if not skip_migration and not is_migration_script():
        ensure_db_version(
            config.registry.settings['config_uri'], get_session_maker())

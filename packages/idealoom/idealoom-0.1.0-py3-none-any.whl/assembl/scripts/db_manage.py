""" Wrapper over the command line migrate tool to better work with
config files. """
from __future__ import print_function
#To test:  python -m assembl.scripts.db_manage
import argparse
import subprocess
import sys
import os
import time
from os.path import join, dirname, exists

from pyramid.paster import get_appsettings
import transaction
from alembic.migration import MigrationContext

from ..lib.migration import bootstrap_db, bootstrap_db_data
from ..lib.sqla import configure_engine, mark_changed
from ..lib.zmqlib import configure_zmq
from ..lib.config import set_config


def main():
    parser = argparse.ArgumentParser(description="Manage database bootstrap, backup and update.")
    parser.add_argument("configuration", help="configuration file")
    parser.add_argument("command", help="command",  choices=['bootstrap', 'backup', 'alembic'])
    parser.add_argument('alembic_args', nargs='*')
    args = parser.parse_args()
    settings = get_appsettings(args.configuration, 'idealoom')
    set_config(settings)
    configure_zmq(settings['changes_socket'], False)
    engine = configure_engine(settings, True)
    if args.command == "bootstrap":
        db = bootstrap_db(args.configuration)
        bootstrap_db_data(db)
        mark_changed()
        transaction.commit()

    elif args.command == "backup":
        projectpath = dirname(dirname(dirname(__file__)))
        dbdumps_dir = join(projectpath, "assembl_dumps")
        if not exists(dbdumps_dir):
            subprocess.check_call('mkdir -m700 ' + dbdumps_dir)

        filename = 'db_%s.sql.pgdump' % time.strftime('%Y%m%d')
        file_path = join(dbdumps_dir, filename)
        pg_dump_path = subprocess.check_output(['which', 'pg_dump']).strip()
        # Dump
        subprocess.check_call(
            [
                pg_dump_path,
                '--host=' + settings['db_host'],
                '-U' + settings['db_user'],
                '--format=custom',
                '-b', settings['db_database'],
                '-f', file_path],
            env={"PGPASSWORD": settings['db_password']})

        # Make symlink to latest
        subprocess.check_call([
            'ln', '-sf', file_path, 'idealoom-backup.pgdump'])

    elif args.command == "alembic":
        context = MigrationContext.configure(engine.connect())
        db_version = context.get_current_revision()

        if not db_version:
            sys.stderr.write('Database not initialized.\n'
                             'Try this: "idealoom-db-manage %s bootstrap"\n'
                             % args.configuration)
            sys.exit(2)

        cmd = ['alembic', '-c', args.configuration] + args.alembic_args

        print(subprocess.check_output(cmd))


if __name__ == '__main__':
    main()

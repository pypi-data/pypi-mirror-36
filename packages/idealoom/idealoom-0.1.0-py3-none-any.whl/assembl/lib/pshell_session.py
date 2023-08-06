"""Initial objects for the pshell sessions"""
from __future__ import absolute_import
import sys

from pyramid.paster import get_appsettings
from .sqla import get_session_maker, configure_engine
from assembl.semantic import upgrade_semantic_mapping as _usm
from assembl.lib.config import set_config as _set_config

# an implicit session for pshell
app_settings = get_appsettings(sys.argv[1], 'idealoom')
_set_config(app_settings)
configure_engine(app_settings, False)
db = get_session_maker()
_usm()

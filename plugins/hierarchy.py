"""OpenHLtest DotNet interface generation plugin

    - uses c# yang interfaces and custom attributes
"""

import optparse
import sys
import os
import glob
import re
import logging
import time
import json
from pyang import plugin
from pyang import statements

def pyang_plugin_init():
    plugin.register_plugin(HierarchyPlugin())

class HierarchyPlugin(plugin.PyangPlugin):
    """Generates json hierarchy:
    """
    _plugin_name = 'hierarchy'

    def __init__(self):
        """Called by pyang"""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        handlers = [logging.StreamHandler(sys.stdout)]
        formatter = logging.Formatter(fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        formatter.converter = time.gmtime
        for handler in handlers:
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.info('current working directory: %s' % os.getcwd())
        plugin.PyangPlugin.__init__(self, HierarchyPlugin._plugin_name)
        self._classes = {}
        self._base_output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '../doc-browser/src/assets'))
        self._logger.info('hierarchy output: %s' % self._base_output_dir)
        
    def add_output_format(self, fmts):
        """Called by pyang"""
        self.multiple_modules = True
        fmts[HierarchyPlugin._plugin_name] = self

    def add_opts(self, optparser):
        """Called by pyang"""
        pass

    def setup_ctx(self, ctx):
        """Called by pyang"""
        try:
            os.remove(ctx.opts.outfile)
        except Exception as e:
            self._logger.info(e)

    def setup_fmt(self, ctx):
        """Called by pyang"""
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        """Called by pyang.s
        This starts the process of creating skeleton classes.

        Args:
            ctx: The context
            modules: The module specified in the command line
            fd: A file descriptor setup by pyang specified in the command line
        """
        # start at the top level and iterate down, lets build our own hierarchy, basis for docs
        hierarchy = []
        self._module = modules[0]
        self._nextId = 0
        self._build_hierarchy(self._module, hierarchy)
        json.dump(hierarchy, fd, indent=4)

    def _build_hierarchy(self, stmt, hierarchy):
        """Build up a hierarchical dictionary of the yang model.

        Args:
            stmt (Statement): A pyang statement object
            hierarchy (dict): The hierarchy that the statement should be added to 
        """
        self._nextId += 1
        entry = self._build_hierarchy_entry(stmt)
        hierarchy.append(entry)
        if stmt.keyword in ['module', 'list', 'container', 'rpc', 'action', 'input', 'output']:
            if stmt.i_children is not None and len(stmt.i_children) > 0:
                entry['children'] = []
                for child_stmt in stmt.i_children:
                    self._build_hierarchy(child_stmt, entry['children'])

    def _build_hierarchy_entry(self, stmt):
        entry = {
            'id': self._nextId,
            'name': stmt.arg,
            '_keyword': stmt.keyword,
            '_path': self._get_yang_path(stmt),
            '_status': self._get_yang_status(stmt),
            '_description': self._get_yang_description(stmt),
            '_writeable': self._get_yang_writeable(stmt)
        }
        self._add_yang_key(stmt, entry)	
        self._add_yang_type(stmt, entry)
        self._add_yang_presence(stmt, entry)
        return entry

    def _add_yang_presence(self, stmt, entry):
        yang_presence = stmt.search_one('presence')
        if yang_presence is not None:
            entry['_container_presence'] = yang_presence.arg

    def _add_yang_type(self, stmt, entry):
        yang_type = stmt.search_one('type')
        if yang_type is None:
            return
        else:
            entry['_type'] = yang_type.arg
        if yang_type.arg == 'enumeration':
            enums = []
            for enum in yang_type.search('enum'):
                enums.append( {
                    'name': enum.arg,
                    'description': self._get_yang_description(enum)
                })
            entry['_type_enums'] = enums
        if yang_type.arg == 'leafref':
            paths = []
            for path in yang_type.search('path'):
                paths.append(path.arg)
            entry['_type_paths'] = paths

    def _add_yang_key(self, stmt, entry):
        yang_key = stmt.search_one('key')
        if yang_key is not None:
            entry['_key'] = yang_key.arg

    def _get_yang_writeable(self, stmt):
        if hasattr(stmt, 'i_config') is False:
            return True
        if stmt.i_config is None:
            return True
        return stmt.i_config

    def _is_blank(self, value):
        return not(value and value.arg.strip())

    def _get_yang_path(self, stmt):
        if stmt.parent is not None:
            return '%s:%s' % (self._module.i_prefix, statements.mk_path_str(stmt)[1:])
        else:
            return self._module.i_prefix

    def _get_yang_description(self, stmt):
        description = stmt.search_one('description')
        if self._is_blank(description):
            return 'TBD'
        else:
            return description.arg

    def _get_yang_status(self, stmt):
        status = stmt.search_one('status')
        if status is None or status.arg == 'current':
            return 'current'
        else:
            return status.arg

    def _get_yang_leafref_path(self, s):
        t = s.search_one('type')
        if t is not None:
            if t.arg == 'leafref':
                return t.search_one('path')
        else:
            return None

    def _get_typename(self, s):
        t = s.search_one('type')
        if t is not None:
            if t.arg == 'leafref':
                p = t.search_one('path')
                if p is not None:
                    # Try to make the path as compact as possible.
                    # Remove local prefixes, and only use prefix when
                    # there is a module change in the path.
                    target = []
                    curprefix = s.i_module.i_prefix
                    for name in p.arg.split('/'):
                        if name.find(":") == -1:
                            prefix = curprefix
                        else:
                            [prefix, name] = name.split(':', 1)
                        if prefix == curprefix:
                            target.append(name)
                        else:
                            target.append(prefix + ':' + name)
                            curprefix = prefix
                    return "-> %s" % "/".join(target)
                else:
                    return t.arg
            else:
                return t.arg
        elif s.keyword == 'anydata':
            return '<anydata>'
        elif s.keyword == 'anyxml':
            return '<anyxml>'
        else:
            return ''


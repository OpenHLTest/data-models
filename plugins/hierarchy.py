"""OpenHLtest JSON documentation generator
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
from pyang import types
from pyang import statements


def pyang_plugin_init():
    plugin.register_plugin(HierarchyPlugin())


class HierarchyPlugin(plugin.PyangPlugin):
    """Generates a json hierarchy that is used for documentation and python client generation
    """
    _plugin_name = 'hierarchy'

    def __init__(self):
        """Called by pyang"""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        handlers = [logging.StreamHandler(sys.stdout)]
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        formatter.converter = time.gmtime
        for handler in handlers:
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.info('current working directory: %s' % os.getcwd())
        plugin.PyangPlugin.__init__(self, HierarchyPlugin._plugin_name)
        self._classes = {}
        self._base_output_dir = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '../doc-browser/src/assets'))
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
            self._ctx = ctx
            os.remove(ctx.opts.outfile)
        except Exception as e:
            self._logger.info(e)

    def setup_fmt(self, ctx):
        """Called by pyang"""
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        """Called by pyang
        This starts the process of creating the hierarhcy.

        Args:
            ctx: The context
            modules: The module specified in the command line
            fd: A file descriptor setup by pyang specified in the command line
        """
        # start at the top level and iterate down, lets build our own hierarchy, basis for docs
        self._logger.info('hierarchy build start')
        hierarchy = []
        self._module = modules[0]
        self._nextId = 0
        self._build_hierarchy(self._module, hierarchy)
        self._logger.info('hierarchy build complete')
        self._logger.info('write json file start')
        json.dump(hierarchy, fd, indent=4)
        fd.close()
        self._logger.info('write json file complete')

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
        """Create a hierarchy entry

        Required keys:
            id: a unique numeric id
            name: keyword argument
            _keyword: the yang keyword
            _path: the full yang path
            _status: the status of the yang statement
            _description: the description of the yang statement
            _writeable: the configurability of the yang statement

        Optional keys (depending on keyword):
            _unsupported_feature: can exist on any keyword
            _key: substmt of list
            _presence: substmt of container
            _type: substmt of leaf, leaf-list
            _type_pattern: substmt of type
            _enums: substmt of enumeration
            _leafref_paths: substmt of leafref
            _constraint: substmt must
            _when: substmt when
        """
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
        self._add_yang_constraint(stmt, entry)
        self._add_yang_type(stmt, entry)
        self._add_yang_presence(stmt, entry)
        self._add_unsupported_feature(stmt, entry)
        return entry

    def _add_unsupported_feature(self, stmt, entry):
        unsupported_feature = []
        for substmt in stmt.substmts:
            if hasattr(substmt, 'i_extension') is True:
                unsupported_feature.append(substmt.i_extension.arg)
        if len(unsupported_feature) > 0:
            entry['_unsupported_feature'] = unsupported_feature

    def _add_yang_constraint(self, stmt, entry):
        yang_must = stmt.search_one('must')
        if yang_must is not None:
            entry['_constraint'] = statements.mk_path_str(yang_must)
        yang_when = stmt.search_one('when')
        if yang_when is not None:
            entry['_when'] = yang_when.arg

    def _add_yang_presence(self, stmt, entry):
        yang_presence = stmt.search_one('presence')
        if yang_presence is not None:
            entry['_presence'] = yang_presence.arg

    def _add_yang_type(self, stmt, entry):
        if stmt is None:
            return
        yang_type = stmt.search_one('type')
        if yang_type is None:
            return
        entry['_type'] = yang_type.arg
        if hasattr(stmt, 'i_default_str') and stmt.i_default_str is not None:
            entry['_type_pattern'] = stmt.i_default_str
        if yang_type.arg == 'enumeration':
            enums = []
            for enum in yang_type.search('enum'):
                enum_entry = {
                        'name': enum.arg,
                        'description': self._get_yang_description(enum)
                    }
                self._add_unsupported_feature(enum, enum_entry)
                enums.append(enum_entry)
            entry['_enums'] = enums
        if yang_type.arg == 'leafref':
            paths = []
            self._validate_leaf_ref(stmt, yang_type, paths)
            entry['_leafref_paths'] = paths
        if yang_type.arg == 'union':
            paths = []
            for leafref in yang_type.i_type_spec.types:
                self._validate_leaf_ref(stmt, leafref, paths)
            entry['_type'] = 'union[leafref]'
            entry['_leafref_paths'] = paths
        pattern = yang_type.search_one('pattern')
        if pattern is not None:
            entry['_type_pattern'] = pattern.arg
        if hasattr(yang_type, 'i_typedef') and yang_type.i_typedef is not None:
            entry['_typedef'] = yang_type.i_typedef.arg
            self._add_yang_type(yang_type.i_typedef, entry)

    def _validate_leaf_ref(self, stmt, leafref, paths):
        if isinstance(leafref.i_type_spec, types.EmptyTypeSpec) is True:
            paths.append('null')
        else:
            validation = statements.validate_leafref_path(
                self._ctx, stmt, leafref.i_type_spec.path_spec, leafref.i_type_spec.path_)
            if validation is None:
                failed_validation = '%s leafref path %s is bad' % (
                    statements.mk_path_str(stmt), leafref.i_type_spec.path_.arg)
                self._logger.error(failed_validation)
                paths.append('Failed validation: ' +
                             leafref.i_type_spec.path_.arg)
            else:
                paths.append(statements.mk_path_str(validation[0]))

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
            return '%s:%s' % (self._module.arg, statements.mk_path_str(stmt)[1:])
        else:
            return self._module.arg

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

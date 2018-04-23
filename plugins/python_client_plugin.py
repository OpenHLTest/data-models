"""OpenHLtest pyang plugin
    Generates OpenHlTest python client code
"""

import optparse
import sys
import os
import glob
import re

from pyang import plugin
from pyang import statements

def pyang_plugin_init():
    plugin.register_plugin(OpenHlTestPythonClient())

class OpenHlTestPythonClient(plugin.PyangPlugin):
    _plugin_name = 'openhltest'

    def __init__(self):
        plugin.PyangPlugin.__init__(self, OpenHlTestPythonClient._plugin_name)
        self._base_output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '../python_client/openhltest'))
        print('outputting client classes to %s' % self._base_output_dir)
        
    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts[OpenHlTestPythonClient._plugin_name] = self

    def add_opts(self, optparser):
        optlist = []
        # if plugin.is_plugin_registered('restconf'):
        #     optlist.append(
        #         optparse.make_option("--tree-print-yang-data",
        #                              dest="tree_print_yang_data",
        #                              action="store_true",
        #                              help="Print ietf-restconf:yang-data " +
        #                              "structures")
        #     )
        # g = optparser.add_option_group("Tree output specific options")
        # g.add_options(optlist)

    def setup_ctx(self, ctx):
        pass

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        self._fid = fd
        if ctx.opts.tree_path is not None:
            path = ctx.opts.tree_path.split('/')
            if path[0] == '':
                path = path[1:]
        else:
            path = None

        self._emit_classes(ctx, modules, fd, ctx.opts.tree_depth, path)

    def _emit_classes(self, ctx, modules, fd, depth, path):
        self._write_line('from httptransport import HttpTransport')
        self._write_line('from yangbase import YangBase')
        self._write_line()
        self._write_line()
        
        for module in modules:
            self._write_python_class(module, module)

            children = []
            for child in module.i_children:
                if child.keyword in statements.data_definition_keywords:
                    children.append(child)
            if path is not None and len(path) > 0:
                children = [child for child in children if child.arg == path[0]]
                path = path[1:]

            if len(children) > 0:
                self._print_children(children, module, fd, '  ', path, 'data', depth)

            mods = [module]
            for i in module.search('include'):
                subm = ctx.get_module(i.arg)
                if subm is not None:
                    mods.append(subm)
            for m in mods:
                section_delimiter_printed = False
                for augment in m.search('augment'):
                    if (hasattr(augment.i_target_node, 'i_module') and
                            augment.i_target_node.i_module not in modules + mods):
                        if not section_delimiter_printed:
                            fd.write('\n')
                            section_delimiter_printed = True
                        # this augment has not been printed; print it
                        if not printed_header:
                            print_header()
                            printed_header = True
                        fd.write("  augment %s:\n" % augment.arg)
                        self._print_children(augment.i_children, m, fd, '  ', path, 'augment', depth)

            rpcs = [child for child in module.i_children if child.keyword == 'rpc']
            if path is not None:
                if len(path) > 0:
                    rpcs = [rpc for rpc in rpcs if rpc.arg == path[0]]
                    path = path[1:]
                else:
                    rpcs = []
            if len(rpcs) > 0:
                self._print_children(rpcs, module, fd, '  ', path, 'rpc', depth)

            notifs = [child for child in module.i_children if child.keyword == 'notification']
            if path is not None:
                if len(path) > 0:
                    notifs = [n for n in notifs if n.arg == path[0]]
                    path = path[1:]
                else:
                    notifs = []
            # if len(notifs) > 0:
                # fd.write("\n  notifications:\n")
                #self._print_children(notifs, module, fd, '  ', path, 'notification', depth, llen)

            # if len(module.i_groupings) > 0:
            # 	section_delimiter_printed = False
            # 	for gname in module.i_groupings:
            # 		if not section_delimiter_printed:
            # 			fd.write('\n')
            # 			section_delimiter_printed = True
            # 		fd.write("  grouping %s\n" % gname)
            # 		g = module.i_groupings[gname]
            # 		statements.print_tree(g, substmts=True, i_children=False, indent=4)
                    # self._print_children(g.i_children, module, fd,
                    # 			'  ', path, 'grouping', depth, llen)

    def _print_children(self, i_children, module, fd, prefix, path, mode, depth):
        for child in i_children:
            if ((child.keyword == 'input' or child.keyword == 'output') and len(child.i_children) == 0):
                pass
            else:
                if (child == i_children[-1] or (i_children[-1].keyword == 'output' and len(i_children[-1].i_children) == 0)):
                    # the last test is to detect if we print input, and the
                    # next node is an empty output node; then don't add the |
                    newprefix = prefix + '   '
                else:
                    newprefix = prefix + '  |'
                if child.keyword == 'input':
                    mode = 'input'
                elif child.keyword == 'output':
                    mode = 'output'

                self._print_node(child, module, fd, newprefix, path, mode, depth)

    def _is_blank(self, value):
        return not(value and value.arg.strip())

    def _get_yang_path(self, stmt, module):
        return statements.mk_path_str(stmt)[1:]

    def _get_yang_name(self, name):
        yang_name = ''
        for piece in name.split('-'):
            yang_name = '%s%s%s' % (yang_name, piece[0:1].upper(), piece[1:])
        return yang_name

    def _get_yang_description(self, stmt):
        yang_description = stmt.search_one('description')
        if self._is_blank(yang_description):
            yang_description = 'TBD'
        else:
            yang_description = yang_description.arg.replace('\n', ' ')
        return yang_description

    def _add_abstract_class(self, stmt, module):
        yang_path = self._get_yang_path(stmt, module)
        print(yang_path)
        yang_name = self._get_yang_name(stmt.arg)
        yang_description = self._get_yang_description(stmt)
        
        interface_name = None

        yang_children = ''
        for child in stmt.i_children:
            if child.keyword in ['container', 'list']:
                yang_children = '%s, "%s"' % (yang_children, child.arg)
        yang_children = yang_children.strip(',').strip()

        if stmt.keyword in ['container', 'list']:
            self._write_python_class(module, stmt)

    def _get_key_name(self, stmt):
        yang_key = stmt.search_one('key')
        if yang_key is not None:
            return yang_key.arg
        else:
            return None

    def _get_python_class_name(self, module, stmt):
        python_class_name = ''
        yang_path = self._get_yang_path(stmt, module)
        pieces = yang_path.split('/')
        for piece in pieces:
            if ':' in piece:
                continue
            python_class_name = '%s%s' % (python_class_name, self._get_yang_name(piece))
        return python_class_name

    def _write_python_class(self, module, stmt):
        if module == stmt:
            python_class_name = self._get_yang_name(module.arg)
        else:
            python_class_name = self._get_python_class_name(module, stmt)

        self._write_line("class %s(YangBase):" % python_class_name)
        self._write_line('\t"""%s' % self._get_yang_description(stmt))
        self._write_line('\t"""')

        if module == stmt:
            self._write_line("\tdef __init__(self, ip_address, rest_port):")
        elif stmt.keyword == 'list':
            self._write_line("\tdef __init__(self, parent, yang_key_value=None):")
        else:
            self._write_line("\tdef __init__(self, parent):")

        if module == stmt:
            YANG_MODULE = ''
            YANG_CLASS = ''
        else:
            YANG_MODULE = module.arg
            YANG_CLASS = stmt.arg
        self._write_line("\t\tself.YANG_MODULE = '%s'" % YANG_MODULE)
        self._write_line("\t\tself.YANG_CLASS = '%s'" % YANG_CLASS)

        key = self._get_key_name(stmt)
        if module == stmt:
            self._write_line("\t\tsuper(%s, self).__init__(HttpTransport(ip_address, rest_port), None)" % python_class_name)
        elif stmt.keyword == 'list' and key is not None:
            self._write_line("\t\tself.YANG_KEY = '%s'" % key)
            self._write_line("\t\tsuper(%s, self).__init__(parent, yang_key_value)" % python_class_name)
        else:
            self._write_line("\t\tsuper(%s, self).__init__(parent, None)" % python_class_name)

        self._write_class_child_gets(module, stmt)
        self._write_class_properties(module, stmt)
        self._write_class_actions(module, stmt)

        self._write_line()
        self._write_line()            

    def _write_class_child_gets(self, module, stmt):
        # methods for accessing child container/list keywords
        for child in stmt.i_children:
            if child.keyword in ['container', 'list']:
                key_name = self._get_key_name(child)
                python_class_name = self._get_python_class_name(module, child)
                self._write_line()
                if key_name is not None:
                    self._write_line("\tdef %s(self, %s=None):" %(child.arg.replace('-', '_'), key_name))
                    self._write_line('\t\t"""Get the %s object(s) from the server.' %(child.arg))
                    self._write_line()
                    self._write_line("\t\t%s" % self._get_yang_description(child))
                    self._write_line()
                    self._write_line("\t\tArgs:  ")
                    self._write_line("\t\t\t%s (:obj:`str`, optional, default=None): A key value in the %s list.  " %(key_name, child.arg))
                    self._write_line()
                    self._write_line("\t\tReturns:  ")
                    self._write_line("\t\t\t:obj:`list` of :obj:`%s` | :obj:`%s`: If arg %s is None a list of %s objects otherwise a single %s object.  " % (python_class_name, python_class_name, key_name, python_class_name, python_class_name))
                    self._write_line()
                    self._write_line("\t\tRaises:  ")
                    self._write_line("\t\t\tNotFoundError: %s is not in the list of %s objects.  " % (key_name, child.arg))
                    self._write_line("\t\t\tServerError: An abnormal server error has occurred.  ")
                    self._write_line('\t\t"""')
                    self._write_line("\t\treturn self._read(%s(self, %s))" %(python_class_name, key_name))

                    self._write_line()
                    self._write_line("\tdef create_%s(self, %s):" %(child.arg.replace('-', '_'), key_name))
                    self._write_line('\t\t"""Create a %s instance on the server.' %(child.arg))
                    self._write_line()
                    self._write_line("\t\t%s" % self._get_yang_description(child))
                    self._write_line()
                    self._write_line("\t\tArgs:  ")
                    self._write_line("\t\t\t%s (str): A unique key value that does not exist in the list on the server.  " %(key_name))
                    self._write_line()
                    self._write_line("\t\tReturns:  ")
                    self._write_line("\t\t\t:obj:`%s`: An object encapsulating an instance of the %s model.  " % (python_class_name, child.arg))
                    self._write_line()
                    self._write_line("\t\tRaises:  ")
                    self._write_line("\t\t\tAlreadyExistsError: An instance of %s with the supplied key value already exists on the server.  " % (child.arg))
                    self._write_line("\t\t\tServerError: An abnormal server error has occurred.  ")
                    self._write_line('\t\t"""')
                    self._write_line("\t\treturn self._create(%s(self, %s), locals())" % (python_class_name, key_name))

                else:
                    self._write_line("\tdef %s(self):" % (child.arg.replace('-', '_')))
                    self._write_line('\t\t"""Get the %s object from the server' % child.arg)
                    self._write_line()
                    self._write_line("\t\t%s" % self._get_yang_description(child))
                    self._write_line()
                    self._write_line("\t\tReturns:  ")
                    self._write_line("\t\t\t:obj:`%s`: An object encapsulating an instance of the %s model.  " % (python_class_name, child.arg))
                    self._write_line()
                    self._write_line("\t\tRaises:  ")
                    self._write_line("\t\t\tServerError: An abnormal server error has occurred.  ")
                    self._write_line('\t\t"""')
                    self._write_line("\t\treturn self._read(%s(self))" % python_class_name)

    def _write_class_properties(self, module, stmt):
        for child in stmt.i_children:
            if child.keyword == 'leaf':
                property_name = child.arg.replace('-', '_')
                self._write_line()
                self._write_line("\t@property")
                self._write_line("\tdef %s(self):" %(property_name))
                typename = self._get_typename(child)
                property_docstring = '\t\t"""%s: %s' %(typename, self._get_yang_description(child))
                if '`enum`' in typename:
                    property_docstring += '  \n\t\tEnums:'
                    for enum in child.search_one('type').search('enum'):
                        property_docstring += '  \n\t\t\t%s: %s' %(enum.arg, self._get_yang_description(enum))
                    property_docstring += '  \n\t\t"""'
                else:
                    property_docstring += '"""'
                self._write_line(property_docstring)
                self._write_line("\t\treturn self._get_value('%s')" % (child.arg))

                if child.i_config is True and child.arg != self._get_key_name(stmt):
                    self._write_line()
                    self._write_line("\t@%s.setter" % property_name)
                    self._write_line("\tdef %s(self, value):" % (child.arg.replace('-', '_')))
                    self._write_line("\t\treturn self._set_value('%s', value)" % (child.arg))

    def _write_class_actions(self, module, stmt):
        for child in stmt.i_children:
            if child.keyword == 'action':
                io_details = self._write_input_output(module, child)
                input_arg = ''
                if io_details['input'] is not None:
                    input_arg = ', %s' % (self._to_snake_case(io_details['input']))
                action_name = child.arg.replace('-', '_')
                self._write_line()
                self._write_line("\tdef %s(self%s):" % (action_name, input_arg))
                self._write_line('\t\t"""Execute the %s action on the server' % child.arg)
                self._write_line()
                self._write_line("\t\t%s" % self._get_yang_description(child))
                self._write_line()
                self._write_line("\t\t:return: %s.  " % (io_details['output']))
                self._write_line("\t\t:raises ServerException: An abnormal server error has occurred.  ")
                self._write_line('\t\t"""')
                self._write_line("\t\treturn self._execute(self.url + '/%s'%s)" % (child.arg, input_arg))

    def _write_input_output(self, module, stmt):
        io_details = {
            'input': None,
            'output': None
        }
        for child in stmt.i_children:
            if child.keyword in['input', 'output'] and len(child.i_children) > 0:
                self._write_line()
                io_class_name = '%s%s' % (self._get_yang_name(stmt.arg), self._get_yang_name(child.keyword))
                self._write_line("\tclass %s(object):" % (io_class_name))  
                self._write_line("\t\tdef __init__(self):")
                self._write_line("\t\t\tself.YANG_PATH = '%s:%s'" %(module.arg, child.keyword))
                io_details[child.keyword] = io_class_name
        return io_details

    def _write_line(self, line = ""):
        self._fid.write(line + '\n')

    def _to_snake_case(self, not_snake_case):
        final = ''
        for i in xrange(len(not_snake_case)):
            item = not_snake_case[i]
            if i < len(not_snake_case) - 1: next_char_will_be_underscored = (not_snake_case[i+1] == "_" or not_snake_case[i+1] == " " or not_snake_case[i+1].isupper())
            if (item == " " or item == "_") and next_char_will_be_underscored:
                continue
            elif (item == " " or item == "_"):
                final += "_"
            elif item.isupper():
                final += "_"+item.lower()
            else:
                final += item
        if final[0] == "_":
            final = final[1:]
        return final

    def _print_node(self, s, module, fd, prefix, path, mode, depth):
        if s.i_module.i_modulename == module.i_modulename:
            name = s.arg
        else:
            name = s.i_module.i_prefix + ':' + s.arg
        flags = self._get_flags_str(s, mode)

        # list+config(RwListAttribute), list+noconfig(RoListAttribute), container(ContainerAttribute), case(OptionalContainerAttribute)
        if s.keyword == 'list' or s.keyword == 'container' or s.keyword == 'choice':
            self._add_abstract_class(s, module)
        elif s.keyword == 'action':
            # print('action')
            # self._add_abstract_class(s, module)
            pass
        else:
            # self._add_abstract_class(s, module)
            pass

        if s.keyword == 'list' and s.search_one('key') is not None:
            keystr = " [%s]" % re.sub('\s+', ' ', s.search_one('key').arg)

        features = s.search('if-feature')
        featurenames = [f.arg for f in features]
        if hasattr(s, 'i_augment'):
            afeatures = s.i_augment.search('if-feature')
            featurenames.extend([f.arg for f in afeatures
                                 if f.arg not in featurenames])

        if len(featurenames) > 0:
            fstr = " {%s}?" % ",".join(featurenames)

        #fd.write(line + '\n')
        if hasattr(s, 'i_children'):
            if depth is not None:
                depth = depth - 1
            children = s.i_children
            if path is not None and len(path) > 0:
                children = [child for child in children
                       if child.arg == path[0]]
                path = path[1:]
            if s.keyword in ['action']:
                # print('not descending action at this time')
                pass
            elif s.keyword in ['choice', 'case']:
                self._print_children(children, module, fd, prefix, path, mode, depth)
            else:
                self._print_children(children, module, fd, prefix, path, mode, depth)

    def _get_status_str(self, s):
        status = s.search_one('status')
        if status is None or status.arg == 'current':
            return '+'
        elif status.arg == 'deprecated':
            return 'x'
        elif status.arg == 'obsolete':
            return 'o'

    def _get_flags_str(self, s, mode):
        if mode == 'input':
            return "-w"
        elif s.keyword in ('rpc', 'action', ('tailf-common', 'action')):
            return '-x'
        elif s.keyword == 'notification':
            return '-n'
        elif s.i_config == True:
            return 'rw'
        elif s.i_config == False or mode == 'output' or mode == 'notification':
            return 'ro'
        else:
            return '--'

    def _get_leafref_path(self, s):
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
            elif t.arg == 'anydata':
                return '<anydata>'
            elif t.arg == 'anyxml':
                return '<anyxml>'
            elif t.arg == 'string':
                return 'str'
            elif t.arg == 'enumeration':
                return ':str:`enum`'
            elif t.arg == 'boolean':
                return 'bool'
            elif t.arg == 'binary':
                return ':str:`base64 encoded`'
            else:
                return t.arg
        else:
            return 'str'



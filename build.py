import sys
import os
import subprocess
import glob
import shutil
from setuptools import setup, find_packages
import distutils
import re
import json
import tempfile
import stat


class CiBuild(object):
    """The continuous integration build.
    
    It does the following:
        - checks for any changed model files
        - generates the hierarchical documentation.json 
        - generates the python wheel 
        - builds the angular documentation app
        - posts the python wheel
    """

    def __init__(self):
        self._root_model = 'openhltest.yang'
        if os.name == 'nt':
            self._root_dir = os.path.normpath(os.path.dirname(__file__))
        else:
            self._root_dir = os.getcwd()
        print('root dir location %s' % self._root_dir)
        self._python = os.path.normpath(sys.executable)
        self._python_dir = os.path.dirname(self._python)
        self._view_models_dir = os.path.normpath('%s/views' % self._root_dir)
        self._doc_file = os.path.normpath('%s/doc-browser/src/assets/documentation.json' % self._root_dir)
        self._python_client_dir = os.path.normpath('%s/openhltest_client' % self._root_dir)
        if 'TRAVIS' in os.environ:
            self._openhltest_dir = os.path.normpath(os.path.join(os.environ['TRAVIS_BUILD_DIR'], '../'))
        else:
            self._openhltest_dir = os.path.normpath(os.path.join(self._root_dir, '../'))
        print('openhltest dir location %s' % self._openhltest_dir)
        self._openhltest_github_io_dir = os.path.normpath(os.path.join(self._openhltest_dir, 'OpenHLTest.github.io'))
        print('openhltest doc dir location %s' % self._openhltest_github_io_dir)
        print('reading version...')
        with open(os.path.normpath(os.path.join(self._python_client_dir, 'version.txt'))) as fid:
            self._build_number = fid.read()
        print('building client version %s' % self._build_number)
        if os.name == 'nt':
            self._pyang = os.path.normpath('%s/scripts/pyang' % self._python_dir)
            self._pip = os.path.normpath('%s/Scripts/pip' % self._python_dir)
        else:
            self._pyang = self._find('pyang', "/") 
            #os.path.normpath('%s/..' % self._python_dir))
            self._pip = 'pip'
        self._pluginsdir = os.path.normpath('%s/plugins' % self._root_dir)
        if 'TRAVIS_BRANCH' in os.environ.keys():
            self._branch = os.environ['TRAVIS_BRANCH']
        else:
            self._branch = 'master'
        self._commit_range = None
        if 'TRAVIS_COMMIT_RANGE' in os.environ.keys():
            self._commit_range = os.environ['TRAVIS_COMMIT_RANGE']
        print('pyang location %s' % self._pyang)
        print('pip location %s' % self._pip)
        print('doc file location %s' % self._doc_file)
        self._data_models_dir = os.path.normpath('%s/models' % self._root_dir)
        print('data models location %s' % self._data_models_dir)

        if 'TRAVIS' in os.environ:
            process_args = [
                'git',
                'config',
                'credential.helper',
                'store'
            ]
            if self._run_process(process_args, self._root_dir) > 0:
                print('failed to config credential store')
                sys.exit(-1)
            print('cloning OpenHLTest.github.io...')
            process_args = [
                'git',
                'clone',
                'https://%s@github.com/OpenHLTest/OpenHLTest.github.io.git' % os.environ['GH_TOKEN']
            ]
            if self._run_process(process_args, self._openhltest_dir) > 0:
                print('failed to clone OpenHLTest.github.io')
                sys.exit(-1)

        if os.name == 'nt':
            print('install pyang package...')
            process_args = [
                self._pip,
                'install',
                '--upgrade',
                'pyang'
            ]
            self._run_process(process_args, self._root_dir)
            print('install setuptools package...')
            process_args = [
                self._pip,
                'install',
                '--upgrade',
                'setuptools'
            ]
            self._run_process(process_args, self._root_dir)
            print('install wheel package...')
            process_args = [
                self._pip,
                'install',
                '--upgrade',
                'wheel'
            ]
            self._run_process(process_args, self._root_dir)
            print('install requests package...')
            process_args = [
                self._pip,
                'install',
                '--upgrade',
                'requests'
            ]
            self._run_process(process_args, self._root_dir)
            print('install twine package...')
            process_args = [
                self._pip,
                'install',
                '--upgrade',
                'twine'
            ]
            self._run_process(process_args, self._root_dir)
        print('init complete')

    def _find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                print(os.path.join(root, name))
        return '/home/travis/virtualenv/python2.7.14/bin/pyang'

    def _walk_and_print(self, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                print(os.path.join(root, name))

    def _run_process(self, process_args, default_dir, redirect_stdout_to=None):
        self._process_output = ''
        fid = None
        if redirect_stdout_to is not None:
            fid = open(os.path.join(default_dir, redirect_stdout_to), 'w')
        if os.name == 'nt':
            shell=True
        else:
            shell=False
        process = subprocess.Popen(process_args, bufsize=1, cwd=default_dir, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.returncode is None:
            stdout_data, stderr_data = process.communicate()
            stdout_data = stdout_data.decode('utf-8')
            stderr_data = stderr_data.decode('utf-8')
            if process.returncode == 0:
                if fid is not None:
                    fid.write(stdout_data)
                    fid.close()
                else:
                    # print(stdout_data)
                    self._process_output += stdout_data
                return 0
            elif process.returncode > 0:
                print('PROCESS FAIL: %s' % stderr_data)
                print(self._process_output)
                return process.returncode
            else:
                if fid is not None:
                    fid.write(stdout_data)
                else:
                    # print(stdout_data)
                    self._process_output += stdout_data

    def check_changed_files(self):
        if 'TRAVIS' not in os.environ:
            return
            
        print('checking for changed files...')
        process_args = [
            'git',
            'diff',
            '--name-only'
        ]
        if self._commit_range is not None:
            process_args.append(self._commit_range)
        if self._run_process(process_args, self._root_dir) == 0:
            continue_build = False
            for changed_file in self._process_output.split('\n'):
                if changed_file.startswith(('build.py', '.travis.yml', 'models/', 'openhltest_client/', 'plugins/', 'doc-browser/')):
                    print('changed file %s' % changed_file)
                    continue_build = True
            if continue_build is False:
                print('stopping build, no model or client generation updates')
                sys.exit(0)
        else:
            print('stopping build, git diff failed')
            sys.exit(1)

    def format_model_files(self):
        for root, dirs, files in os.walk(self._data_models_dir):
            for name in files:
                filename = os.path.join(root, name)
                if os.path.basename(filename).endswith('.yang'):
                    print('reformatting %s...' % filename)
                    temp_filename = '%s.tmp' % filename
                    if os.path.exists(temp_filename):
                        os.chmod(temp_filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                        os.remove(temp_filename)                        
                    hierarchy = [
                        self._pyang,
                        '--format',
                        'yang',
                        '--output',
                        temp_filename,
                        filename
                    ]
                    if os.name == 'nt':
                        hierarchy.insert(0, self._python)
                    self._run_process(hierarchy, self._data_models_dir)
                    if self._is_different(filename, temp_filename):
                        shutil.copy(temp_filename, filename)
                    if os.path.exists(temp_filename):
                        os.chmod(temp_filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                        os.remove(temp_filename)                        
    
    def _is_different(self, filename1, filename2):
        with open(filename1) as fid1:
            with open(filename2) as fid2:
                for line1 in fid1:
                    for line2 in fid2:
                        if line1 != line2:
                            return True
                        break
        return False          

    def generate_hierarchy(self):
        print('generating model hierarchy...')
        hierarchy = [
            self._pyang,
            "--strict",
            "--ietf",
            "--lax-xpath-checks",
            "--print-error-code",
            "--ignore-error",
            "LINT_BAD_MODULENAME_PREFIX_N",
            '--format',
            'hierarchy',
            '--plugindir',
            self._pluginsdir,
            '--output',
            self._doc_file,
            '--path',
            self._data_models_dir,
            self._root_model
        ]
        if os.name == 'nt':
            hierarchy.insert(0, self._python)
        if self._run_process(hierarchy, self._data_models_dir) > 0:
            print('generating hierarchy failed')
            sys.exit(1)

    def generate_python_package(self):
        generated_files_dir = os.path.normpath(os.path.join(self._python_client_dir, 'openhltest'))
        if os.path.exists(generated_files_dir) is True:
            for dir_entry in os.listdir(generated_files_dir):
                full_path = os.path.join(generated_files_dir, dir_entry)
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path, ignore_errors=True)
                elif dir_entry.startswith('openhltest'):
                    os.unlink(full_path)

        with open(self._doc_file, 'r') as fid:
            self._nodes = json.load(fid)
        for node in self._nodes:
            self._generate_python_class(node)
        with open(self._doc_file, 'w') as fid:
            json.dump(self._nodes, fid)

    def _make_python_name(self, yang_name):
        camelCaseName = ''
        for piece in yang_name.split('-'):
            camelCaseName += piece[0].upper() + piece[1:]
        return camelCaseName

    def _make_return_path(self, node, exclude_class_name = False):
        path = node['_path'].lower()
        if path.startswith('openhltest:'):
            path = 'openhltest_client/openhltest/%s' % path[len('openhltest:'):]
        else:
            path = 'openhltest_client/openhltest'
        path = '%s.%s' % (re.sub('\/', '.', path), node['name'])
        if exclude_class_name is False:
            path += '.' + self._make_python_name(node['name'])
        return re.sub('-', '', path)

    def _make_class_path(self, path, exclude_last_piece=True):
        class_path = 'OpenHLTest'
        for piece in path[1:].split('/'):
            if exclude_last_piece is True and path.endswith(piece):
                break
            class_path = '%s.%s' % (class_path, self._make_python_name(piece))
        return class_path

    def _get_node_from_path(self, path):
        node = self._nodes[0]
        for piece in path[1:].split('/'):
            for child in node['children']:
                if child['name'] == piece:
                    if child['_keyword'] in ['leaf', 'leaf-list']:
                        return node
                    node = child
                    break
        return None

    def _format_description(self, format, node, indent, returns=None):
        """
            description formats
                CLASS
                    *description from yang node*
                CLASS_PROPERTY
                    *description from yang node*
                    Returns:
                    Raises:
                PROPERTY 
                    *description from yang node*
                    Returns:
                    Raises: when read/write, this will be patch error codes
                METHOD
                    *description from yang node*
                    Returns:
                    Raises:
                INLINE
                    description from yang node, remove \n\t
        """
        formattedDescription = '\t' * indent + '"""'
        lines = re.sub('(^\n)|(\n$)', '', node['_description']).split('\n')
        for i in range(len(lines)):
            if i > 0:
                formattedDescription += '\t' * indent
            formattedDescription += lines[i] + '\n'
        if format == 'CLASS':
            if node['_keyword'] == 'list':
                formattedDescription += '\n%sThis class supports iterators and encapsulates 0..n instances of the %s resource.\n' % ('\t' * indent, node['_path'])
        if format == 'CLASS_PROPERTY':
            formattedDescription += '\n'
            formattedDescription += '%sGet an instance of the %s class.\n\n' % ('\t' * indent, self._make_python_name(node['name']))
            formattedDescription += '%sReturns:\n' % ('\t' * indent)
            formattedDescription += '%sobj(%s)\n' % ('\t' * (indent + 1), self._make_return_path(node))

        if format == 'PROPERTY':
            get_value = node['_type']
            set_value = get_value
            if node['_keyword'] == 'leaf-list' and '_leafref_paths' in node:
                class_path = self._make_class_path(node['_leafref_paths'][0])
                class_path_with_key = self._make_class_path(node['_leafref_paths'][0], exclude_last_piece=False)
                set_value = 'obj(%s) | list(%s)' % (class_path, class_path_with_key)
                get_value = 'list(%s)' % (class_path_with_key)
            elif  '_enums' in node:
                get_value = []
                for enum in node['_enums']:
                    get_value.append(enum['name'])
                get_value = ' | '.join(get_value)
                set_value = get_value 
            elif node['_keyword'] == 'leaf-list' in node:
                get_value = 'list(%s)' % (get_value)
                set_value = 'list(%s)' % (set_value)
            formattedDescription += '\n'
            formattedDescription += '%sGetter Returns:\n' % ('\t' * indent)
            formattedDescription += '%s%s\n' % ('\t' * (indent + 1), get_value)
            if node['_writeable'] is True:
                formattedDescription += '\n'
                formattedDescription += '%sSetter Allows:\n' % ('\t' * indent)
                formattedDescription += '%s%s\n\n' % ('\t' * (indent + 1), set_value)
                formattedDescription += '%sSetter Raises:\n' % ('\t' * indent)
                formattedDescription += '%sValueError\n' % ('\t' * (indent + 1))
                formattedDescription += '%sInvalidValueError\n' % ('\t' * (indent + 1))

        if format == 'METHOD':
            formattedDescription += '\n'
            if 'children' in node:
                for child in node['children']:
                    if child['_keyword'] == 'input' and 'children' in child:
                        doc_dict = {}
                        self._make_doc_dict(child, doc_dict)
                        formattedDescription += '%sArgs:\n' % ('\t' * indent)
                        formattedDescription += '%sinput (%s)\n\n' % ('\t' * (indent + 1), json.dumps(doc_dict))
                for child in node['children']:
                    if child['_keyword'] == 'output' and 'children' in child:
                        doc_dict = {}
                        self._make_doc_dict(child, doc_dict)
                        formattedDescription += '%sReturns:\n' % ('\t' * indent)
                        formattedDescription += '%s(%s)\n\n' % ('\t' * (indent + 1), json.dumps(doc_dict))
        if format == 'INLINE':
            return re.sub('(\n)|(\t)', '', node['_description'])
        return formattedDescription + '\t' * indent + '"""\n'

    def _make_doc_dict(self, node, doc_dict):
        if 'children' in node:
            for child in node['children']:
                if 'children' in child:
                    doc_dict[child['name']] = {}
                    self._make_doc_dict(child, doc_dict[child['name']])
                else:
                    doc_dict[child['name']] = child['_type']
                self._make_doc_dict(child, doc_dict)

    def _make_property_map(self, node):
        property_map = {}
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['leaf', 'leaf-list']:
                    property_map[self._make_python_name(child['name'])] = child['name']
        return property_map

    def _make_method_list(self, node):
        methods = []
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['rpc', 'action']:
                    methods.append(child['name'])
        return methods

    def _generate_python_class(self, node):
        if node['_keyword']	in ['module', 'list', 'container']:
            classDefinition = ''
            classDefinition += 'from openhltest_client.base import Base\n\n\n'
            classDefinition += 'class %s(Base):\n' % self._make_python_name(node['name'])
            classDefinition += self._format_description('CLASS', node, 1)
            classDefinition += "\tYANG_NAME = '%s'\n" % node['name']
            classDefinition += "\tYANG_KEYWORD = '%s'\n" % node['_keyword']
            list_key = "None"
            if '_key' in node:
                list_key = "'%s'" % node['_key'].split()[0]
            classDefinition += "\tYANG_KEY = %s\n" % list_key
            classDefinition += "\tYANG_PROPERTY_MAP = %s\n" % json.dumps(self._make_property_map(node))
            classDefinition += "\tYANG_ACTIONS = %s\n\n" % json.dumps(self._make_method_list(node))
            classDefinition += self._python_class_init(node)
            classDefinition += self._python_class_properties(node)
            classDefinition += self._python_properties(node)
            classDefinition += self._python_methods(node)
            classDefinition += self._python_crud_methods(node)
            
            # write the class file and corresponding __init__.py
            class_path = self._root_dir
            pieces = self._make_return_path(node, exclude_class_name=True).split('.')
            for piece in pieces[0:-1]:
                class_path = os.path.normpath(os.path.join(class_path, piece))
                if os.path.exists(class_path) == False:
                    os.mkdir(class_path)
            open(os.path.normpath(os.path.join(class_path, '__init__.py')), 'w').close()
            class_filename = os.path.normpath(os.path.join(class_path, '%s.py' % pieces[-1]))
            with open(class_filename, 'w') as fid:
                fid.write(classDefinition)
            node['_python_class'] = classDefinition

            if 'children' in node:
                for child in node['children']:
                    self._generate_python_class(child)

    def _python_class_init(self, node):
        init = ''
        if node['_keyword'] == 'module':
            init += '\tdef __init__(self, transport):\n'
            init += '\t\tsuper(%s, self).__init__(transport)\n\n' % self._make_python_name(node['name'])
        else:
            init += '\tdef __init__(self, parent):\n'
            init += '\t\tsuper(%s, self).__init__(parent)\n\n' % self._make_python_name(node['name'])
        return init      

    def _python_class_properties(self, node):
        classProperties = ''
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['container', 'list']:
                    class_name = self._make_python_name(child['name'])
                    classProperties += '\t@property\n'
                    classProperties += '\tdef %s(self):\n' % class_name
                    classProperties += self._format_description('CLASS_PROPERTY', child, 2)
                    classProperties += '\t\tfrom %s import %s\n' % (self._make_return_path(child, True), class_name)
                    if child['_keyword'] == 'list':
                        classProperties += '\t\treturn %s(self)\n\n' % class_name
                    else:
                        classProperties += '\t\treturn %s(self)._read()\n\n' % class_name
        return classProperties

    def _python_properties(self, node):
        if 'children' not in node:
            return ''
        properties = ''
        for child in node['children']:
            if child['_keyword'] in ['leaf', 'leaf-list']:
                python_name = self._make_python_name(child['name'])
                properties += '\t@property\n'
                properties += '\tdef %s(self):\n' % python_name
                properties += self._format_description('PROPERTY', child, 2)
                properties += "\t\treturn self._get_value('%s')\n" % child['name']
                if node['_keyword'] == 'list' and child['name'] in node['_key']:
                    properties += '\n'
                    continue
                # if child['_writeable']:
                #     properties += '\t@%s.setter\n' % python_name
                #     properties += '\tdef %s(self, value):\n' % python_name
                #     properties += "\t\treturn self._set_value('%s', value)\n\n" % child['name']
                # else:
                properties += '\n'
        return properties

    def _python_methods(self, node):
        methods = ''
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['rpc', 'action']:
                    input_param = ''
                    typedef_params = {
                        "input-file-name": None,
                        "output-file-name": None,
                        "file-content": None
                    }
                    if 'children' in child:
                        for arg_child in child['children']:
                            if arg_child['_keyword'] == 'input' and 'children' in arg_child:
                                input_param = ', input'
                                for inputs in arg_child['children']:
                                    self._get_typedef(inputs, 'input-file-name', typedef_params)
                                    self._get_typedef(inputs, 'output-file-name', typedef_params)
                            if arg_child['_keyword'] == 'output' and 'children' in arg_child:
                                for outputs in arg_child['children']:
                                    self._get_typedef(outputs, 'file-content', typedef_params)
                    methods += '\tdef %s(self%s):\n' % (self._make_python_name(child['name']), input_param)
                    methods += self._format_description('METHOD', child, 2)
                    if typedef_params['input-file-name'] is not None:
                        methods += "\t\twith open(input['%s'], 'rb') as fid:\n" % typedef_params['input-file-name']
                        methods += "\t\t\timport base64\n"
                        methods += "\t\t\tinput['%s'] = base64.b64encode(fid.read())\n" % typedef_params['input-file-name']
                        methods += "\t\treturn self._execute('%s'%s)\n\n" % (child['name'], input_param)
                    elif typedef_params['output-file-name'] is not None and typedef_params['file-content'] is not None:
                        methods += "\t\toutput = self._execute('%s'%s)\n" % (child['name'], input_param)
                        methods += "\t\twith open(input['%s'], 'wb') as fid:\n" % typedef_params['output-file-name']
                        methods += "\t\t\timport base64\n"
                        methods += "\t\t\tfid.write(base64.b64decode(output['%s']))\n" % typedef_params['file-content']
                        methods += "\t\treturn output\n\n"
                    else:
                        methods += "\t\treturn self._execute('%s'%s)\n\n" % (child['name'], input_param)
        return methods
    
    def _get_typedef(self, node, typedef_name, typedef_params):
        if '_typedef' in node and node['_typedef'] == typedef_name:
            typedef_params[typedef_name] = node['name']

    def _get_args(self, node, add_arg_key=True):
        arg_string = ''
        arg_list = []
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['leaf', 'leaf-list']:
                    if len(arg_string) > 0:
                        arg_string += ', '
                    if '_key' in node and node['_key'] == child['name']:
                        if add_arg_key is True:
                            arg_string += '%s' % self._make_python_name(child['name'])
                        else:
                            continue
                    else:
                        arg_string += '%s=None' % self._make_python_name(child['name'])
                    arg_list.append(child)
        return (arg_string, arg_list)

    def _python_crud_methods(self, node):
        crud = ''
        create_args = self._get_args(node)
        update_args = self._get_args(node, add_arg_key=False)

        if node['_keyword'] == 'list':
            key = self._make_python_name(node['_key'].split()[0])
            crud += '\tdef read(self, %s=None):\n' % key
            crud += '\t\t"""Get `%s` resource(s). Returns all `%s` resources from the server if no input parameters are specified.\n\n' % (node['name'], node['name'])
            #crud += '\t\t\t%s (%s): %s\n' % (self._make_python_name(node['name']), arg['_type'], self._format_description('INLINE', arg, 0))
            crud += '\t\t"""\n'                     
            crud += "\t\treturn self._read(%s)\n\n" % key

            if node['_writeable'] is True:
                crud += '\tdef create(self, %s):\n' % create_args[0]
                crud += '\t\t"""Create an instance of the `%s` resource\n\n' % node['name']
                if len(create_args[1]) > 0:
                    crud += '\t\tArgs:\n'
                    for arg in create_args[1]:
                        crud += '\t\t\t%s (%s): %s\n' % (self._make_python_name(arg['name']), arg['_type'], self._format_description('INLINE', arg, 0))
                crud += '\t\t"""\n'
                crud += "\t\treturn self._create(locals())\n\n"

                crud += '\tdef delete(self):\n'
                crud += '\t\t"""Delete all the encapsulated instances of the retrieved `%s` resource\n\n' % node['name']
                crud += '\t\t"""\n'                
                crud += "\t\treturn self._delete()\n\n"

        if node['_keyword'] in ['list', 'container'] and node['_writeable'] is True:
            if len(update_args[0]) > 0:
                crud += '\tdef update(self, %s):\n' % update_args[0]
                crud += '\t\t"""Update the current instance of the `%s` resource\n\n' % node['name']
                if len(update_args[1]) > 0:
                    crud += '\t\tArgs:\n'
                    for arg in update_args[1]:
                        crud += '\t\t\t%s (%s): %s\n' % (self._make_python_name(arg['name']), arg['_type'], self._format_description('INLINE', arg, 0))
                crud += '\t\t"""\n'
                crud += "\t\treturn self._update(locals())\n\n"

        return crud    

    def build_python_package(self):
        os.chdir(self._root_dir)
        print('clean bdist_wheel build artifacts...')
        shutil.rmtree('openhltest_client.egg-info', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        shutil.rmtree('build', ignore_errors=True)

        with open('%s/README.md' % self._root_dir, 'r') as fid:
            long_description = fid.read()

        print('create openhltest python client wheel...')
        from setuptools import setup
        result = setup(name='openhltest',
            version=self._build_number,
            description='OpenHLTest Python Client',
            long_description=long_description,
            long_description_content_type='text/markdown',
            url='https://openhltest.github.io/docs',
            author='OpenHLTest Working Group',
            author_email='andy.balogh@keysight.com',
            license='MIT',
            classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Topic :: Software Development',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3'],
            keywords='openhltest keysight spirent automation',
            packages = find_packages(),
            include_package_data=True,
            python_requires='>=2.7, <4',
            install_requires=['requests'],
            script_name='setup.py',
            script_args=['-q', 'bdist_wheel', '--universal'])

        self._dist_dir = os.path.join(self._root_dir, result.command_obj['bdist_wheel'].dist_dir)
        self._wheel = os.path.basename(result.command_obj['bdist_wheel'].distribution.dist_files[0][2])
        print('%s is ready for posting to pypi' % self._wheel)

    def generate_angular_doc_app(self): 
        self._angular_app_dir = os.path.join(self._root_dir, 'doc-browser')

        print('only build doc browser if angular is installed')
        process_args = [
            'npm',
            'run',
            'ng',
            '-version'
        ]
        if self._run_process(process_args, self._angular_app_dir) > 0:
            print('skipping doc browser build')
            return

        print('update npm...')
        process_args = [
            'npm',
            'install',
            'npm@latest',
            '-g'
        ]
        if self._run_process(process_args, self._angular_app_dir) > 0:
            sys.exit(-1)

        if os.name != 'nt':
            print('update node...')
            process_args = [
                'npm',
                'install',
                '-g',
                'n'
            ]
            if self._run_process(process_args, self._angular_app_dir) > 0:
                sys.exit(-1)

        print('get packages...')
        process_args = [
            'npm',
            'install'
        ]
        if self._run_process(process_args, self._angular_app_dir) > 0:
            sys.exit(-1)

        print('build angular app...')
        process_args = [
            'npm',
            'run',
            'ng',
            'build'
        ]
        if self._run_process(process_args, self._angular_app_dir) > 0:
            sys.exit(-1)

    def deploy_python_package(self):
        if 'TRAVIS' not in os.environ:
            return
            
        print('uploading %s to pypi...' % self._wheel)
        process_args = [
            'twine',
            'upload',
            '-u',
            'abalogh',
            '-p',
            os.environ['PYPI_TOKEN'],
            self._wheel
        ]
        if self._run_process(process_args, self._dist_dir) > 0:
            print('openhltest client package deployment to pypi failed')

    def update_openhltest_github_io(self):
        if 'TRAVIS' not in os.environ:
            return

        os.chdir(self._openhltest_github_io_dir)

        print('git add...')
        process_args = [
            'git',
            'add',
            '-u',
            '-v'
        ]
        self._run_process(process_args, self._openhltest_github_io_dir)

        print('git commit...')
        process_args = [
            'git',
            'commit',
            '-m "update python client documentation"',
            '-a',
            '-v'
        ]
        self._run_process(process_args, self._openhltest_github_io_dir)

        print('git push...')
        process_args = [
            'git',
            'push'
        ]
        self._run_process(process_args, self._openhltest_github_io_dir)

        return 0


cibuild = CiBuild()
cibuild.check_changed_files()
cibuild.format_model_files()
cibuild.generate_hierarchy()
cibuild.generate_python_package()
cibuild.generate_angular_doc_app() 
cibuild.build_python_package()
cibuild.deploy_python_package()
cibuild.update_openhltest_github_io()


import sys
import os
import subprocess
import glob
import shutil
from setuptools import setup, find_packages
import distutils
import re
import json


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
        print('starting openhltest build script __init__')
        self._root_model = 'openhltest.yang'
        self._root_dir = os.getcwd()
        self._python = os.path.normpath(sys.executable)
        self._python_dir = os.path.dirname(self._python)
        self._view_models_dir = os.path.normpath('%s/views' % self._root_dir)
        self._doc_file = os.path.normpath('%s/doc-browser/src/assets/documentation.json' % self._root_dir)
        self._python_client_dir = os.path.normpath('%s/openhltest_client' % self._root_dir)
        print('reading version...')
        with open(os.path.normpath(os.path.join(self._python_client_dir, 'version.txt'))) as fid:
            self._build_number = fid.read()
        print('building client version %s' % self._build_number)
        if os.name == 'nt':
            self._pyang = os.path.normpath('%s/scripts/pyang' % self._python_dir)
            self._pip = os.path.normpath('%s/Scripts/pip' % self._python_dir)
        else:
            self._pyang = self._find('pyang', os.path.normpath('%s/..' % self._python_dir))
        self._pluginsdir = os.path.normpath('%s/plugins' % self._root_dir)
        if 'TRAVIS_BRANCH' in os.environ.keys():
            self._branch = os.environ['TRAVIS_BRANCH']
        else:
            self._branch = 'master'
        self._commit_range = None
        if 'TRAVIS_COMMIT_RANGE' in os.environ.keys():
            self._commit_range = os.environ['TRAVIS_COMMIT_RANGE']
        print('pyang location %s' % self._pyang)
        self._data_models_dir = os.path.normpath('%s/models' % self._root_dir)
        print('data models location %s' % self._data_models_dir)
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
        # process_args = [
        #     'git',
        #     'checkout',
        #     self._branch
        # ]
        # self._run_process(process_args, self._root_dir)
        # process_args = [
        #     'git',
        #     'remote'
        # ]
        # self._run_process(process_args, self._root_dir)
        # process_args = [
        #     'git',
        #     'config',
        #     '--list'
        # ]
        # self._run_process(process_args, self._root_dir)		

    def _find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def _run_process(self, process_args, default_dir, redirect_stdout_to=None):
        self._process_output = ''
        fid = None
        if redirect_stdout_to is not None:
            fid = open(os.path.join(default_dir, redirect_stdout_to), 'w')
        process = subprocess.Popen(process_args, bufsize=1, cwd=default_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.returncode is None:
            stdout_data, stderr_data = process.communicate()
            stdout_data = stdout_data.decode('utf-8')
            stderr_data = stderr_data.decode('utf-8')
            if process.returncode == 0:
                if fid is not None:
                    fid.write(stdout_data)
                    fid.close()
                else:
                    print(stdout_data)
                    self._process_output += stdout_data
                return 0
            elif process.returncode > 0:
                print('PROCESS FAIL: %s' % stderr_data)
                return process.returncode
            else:
                if fid is not None:
                    fid.write(stdout_data)
                else:
                    print(stdout_data)
                    self._process_output += stdout_data

    def _git_add(self, filename):
        print('git add of %s' % filename)
        process_args = [
            'git',
            'add',
            '--all',
            filename
        ]
        self._run_process(process_args, self._root_dir)

    def _git_commit_push(self):
        process_args = [
            'git',
            'commit',
            '-m "upload auto generated model views, python client documentation [skip ci]"'
        ]
        self._run_process(process_args, self._root_dir)
        process_args = [
            'git',
            'push',
            'https://%s@github.com/OpenHLTest/data-models.git' %(os.environ['GH_TOKEN']),
            self._branch
        ]
        self._run_process(process_args, self._root_dir)

    def check_changed_files(self):
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
                if changed_file.startswith('model/') or changed_file.startswith('python_client/') or changed_file.startswith('plugins/'):
                    continue_build = True
            if continue_build is False:
                print('stopping build, no model or client generation updates')
                sys.exit(0)
        else:
            print('stopping build, git diff failed')
            sys.exit(1)

    def generate_hierarchy(self):
        print('generating model hierarchy...')
        hierarchy = [
            self._python,
            self._pyang,
            '--strict',
            '--ietf',
            '--print-error-code',
            '--ignore-error',
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
            nodes = json.load(fid)
        for node in nodes:
            self._generate_python_class(node)

    def _make_python_name(self, yang_name):
        camelCaseName = ''
        for piece in yang_name.split('-'):
            camelCaseName += piece[0].upper() + piece[1:]
        return camelCaseName

    def _make_return_path(self, node, exclude_class_name = False):
        path = node['_path'].lower()
        if len(path) > 4:
            path = 'openhltest_client/openhltest/%s' % path[4:]
        else:
            path = 'openhltest_client/openhltest'
        path = '%s.%s' % (re.sub('\/', '.', path), node['name'])
        if exclude_class_name is False:
            path += '.' + self._make_python_name(node['name'])
        return re.sub('-', '', path)

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
                    *descriptiion from yang node*
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
                formattedDescription += '\n%sImplements the iterator interface __iter__ and encapsulates 0..n instances of the %s resource.\n' % ('\t' * indent, node['_path'])
        if format == 'CLASS_PROPERTY':
                formattedDescription += '\n'
                formattedDescription += '%sGet an instance of the %s class.\n\n' % ('\t' * indent, self._make_python_name(node['name']))
                formattedDescription += '%sReturns:\n' % ('\t' * indent)
                formattedDescription += '%sobj(%s)\n' % ('\t' * (indent + 1), self._make_return_path(node))
        if format == 'PROPERTY':
                formattedDescription += '\n'
                formattedDescription += '%sReturns:\n' % ('\t' * indent)
                formattedDescription += '%s%s\n\n' % ('\t' * (indent + 1), node['_type'])
                formattedDescription += '%sRaises (setter only):\n' % ('\t' * indent)
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
                list_key = "'%s'" % node['_key']
            classDefinition += "\tYANG_KEY = %s\n" % list_key
            classDefinition += "\tYANG_PROPERTY_MAP = %s\n\n" % json.dumps(self._make_property_map(node))
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
            print('generated python class %s' % class_filename)

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
                properties += '\t@%s.setter\n' % python_name
                properties += '\tdef %s(self, value):\n' % python_name
                properties += "\t\treturn self._set_value('%s', value)\n\n" % child['name']
        return properties

    def _python_methods(self, node):
        methods = ''
        if 'children' in node:
            for child in node['children']:
                if child['_keyword'] in ['rpc', 'action']:
                    input_param = ''
                    if 'children' in child:
                        for input_child in child['children']:
                            if input_child['_keyword'] == 'input' and 'children' in input_child:
                                input_param = ', input'
                    methods += '\tdef %s(self%s):\n' % (self._make_python_name(child['name']), input_param)
                    methods += self._format_description('METHOD', child, 2)
                    methods += "\t\treturn self._execute('%s'%s)\n\n" % (child['name'], input_param)
        return methods
    
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
            python_key = self._make_python_name(node['_key'])
            crud += '\tdef create(self, %s):\n' % create_args[0]
            crud += '\t\t"""Create an instance of the `%s` resource\n\n' % node['name']
            if len(create_args[1]) > 0:
                crud += '\t\tArgs:\n'
                for arg in create_args[1]:
                    crud += '\t\t\t%s (%s): %s\n' % (self._make_python_name(arg['name']), arg['_type'], self._format_description('INLINE', arg, 0))
            crud += '\t\t"""\n'
            crud += "\t\treturn self._create(locals())\n\n"

            crud += '\tdef read(self, %s=None):\n' % python_key
            crud += '\t\t"""Get `%s` resource(s). Returns all resources from the server if `%s` is not specified\n\n' % (node['name'], python_key)
            #crud += '\t\t\t%s (%s): %s\n' % (self._make_python_name(node['name']), arg['_type'], self._format_description('INLINE', arg, 0))
            crud += '\t\t"""\n'                     
            crud += "\t\treturn self._read(%s)\n\n" % python_key

            crud += '\tdef delete(self):\n'
            crud += '\t\t"""Delete all the encapsulated instances of the retrieved `%s` resource\n\n' % node['name']
            crud += '\t\t"""\n'                
            crud += "\t\treturn self._delete()\n\n"

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
        result = setup(name='openhltest_client',
            version=self._build_number,
            description='OpenHLTest Python Client',
            long_description=long_description,
            long_description_content_type='text/markdown',
            url='https://openhltest.github.io/docs',
            author='OpenHLTest Working Group',
            author_email='https://github.com/OpenHLTest/data-models/issues',
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
            script_args=['bdist_wheel', '--universal'])

        self._dist_dir = os.path.join(self._root_dir, result.command_obj['bdist_wheel'].dist_dir)
        self._wheel = os.path.basename(result.command_obj['bdist_wheel'].distribution.dist_files[0][2])
        print('%s is ready for distribution' % self._wheel)

    def generate_angular_doc_app(self): 
        print('get npm packages...')
        self._angular_app_dir = os.path.join(self._root_dir, 'doc-browser')
        process_args = [
            'npm',
            'install'
        ]
        self._run_process(process_args, self._angular_app_dir)

        print('build angular app...')
        process_args = [
            'npm',
            'run',
            'ng',
            'build'
        ]
        self._run_process(process_args, self._angular_app_dir)

    def deploy_python_package(self):
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

    def update_repository(self):
        self._openhltest_github_io_dir = os.path.normpath('%s/../OpenHLTest.github.io' % self._root_dir)
        print('openhltest.github.io location %s' % self._openhltest_github_io_dir)
        process_args = [
            'git',
            'checkout',
            self._branch
        ]
        self._run_process(process_args, self._root_dir)
        process_args = [
            'git',
            'remote'
        ]
        self._run_process(process_args, self._root_dir)
        process_args = [
            'git',
            'config',
            '--list'
        ]
        self._run_process(process_args, self._root_dir)	        
        self._git_add()
        print('commit and push of updated files')
        self._git_commit_push()



cibuild = CiBuild()
# cibuild.check_changed_files()
cibuild.generate_hierarchy()
cibuild.generate_python_package()
cibuild.generate_angular_doc_app() 
cibuild.build_python_package()
# cibuild.deploy_python_package()
# cibuild.update_repository()


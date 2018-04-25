"""A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, './openhltest/README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openhltest',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION_NUMBER,

    description='OpenHLTest Python Client',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/openhltest/data-models',

    # Author details
    author='andrey.balogh@gmail.com',
    author_email='andrey.balogh@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='openhltest test tool ixia spirent restconf automation',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = ['openhltest'],
	package_data = {
		'': ['samples/*.py', 'docs/*.*']
	},

    # If your project only runs on certain Python versions, 
    # setting the python_requires argument to the appropriate 
    # PEP 440 version specifier string will prevent pip from installing 
    # the project on other Python versions.s
    python_requires='>=2.7, <4',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
		'requests'
	],
)

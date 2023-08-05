#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import re
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'git-fingerprint'

DESCRIPTION = (
    'Git Fingerprint is a web fingerprinting tool that attempts to scan a '
    'target based on the files a git repository by enumerating over all files '
    'ever found in the public web root and comparing cryptographic hashes of '
    'each commit, branch or tag in order to calculate the best possible match.')

URL = 'https://github.com/Paradoxis/Git-Fingerprint'
EMAIL = 'luke@paradoxis.nl'
AUTHOR = 'Luke Paris (Paradoxis)'
REQUIRES_PYTHON = '>=3.6.0'

REQUIRED = [
    'GitPython==2.1.8',
    'requests==2.18.4',
    'tabulate==0.8.2',
    'axel==0.0.7',
    'progressbar2==3.34.3',
    'dicttoxml==1.7.4'
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = ('\n' + f.read()).strip()


with io.open(os.path.join(here, 'git_fingerprint', '__init__.py'), encoding='utf-8') as init:
    VERSION = re.search(r'__version__ = [\'"]([\d.]+)[\'"]', init.read()).group(1)


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        
        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['git-fingerprint=git_fingerprint.__main__:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)

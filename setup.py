#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Thomas Chiroux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>
#
"""global setup
"""

__authors__ = [
    # alphabetical order by last name
    'Thomas Chiroux', ]

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from io import open
import os
import sys

# local imports
from build_scripts.version import get_git_version

if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0, 'final'):
    raise SystemExit("boksh requires Python 2.7 or later.")

with open("README.rst", encoding='utf-8') as f:
    README = f.read()

with open("NEWS.rst", encoding='utf-8') as f:
    NEWS = f.read()


VERSION = get_git_version()
if VERSION is None:
    try:
        file_name = "boksh/RELEASE-VERSION"
        version_file = open(file_name, "r", encoding='utf-8')
        try:
            VERSION = version_file.readlines()[0]
            VERSION = VERSION.strip()
        except:
            VERSION = "0.0.0"
        finally:
            version_file.close()
    except IOError:
        VERSION = "0.0.0"


class my_build_py(build_py):
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            target_dirs = []
            target_dirs.append(os.path.join(self.build_lib, 'boksh'))
            target_dirs.append('boksh')

            # mkpath is a distutils helper to create directories
            for dir in target_dirs:
                self.mkpath(dir)

            try:
                for dir in target_dirs:
                    fobj = open(os.path.join(dir, 'RELEASE-VERSION'), 'w',
                                encoding='utf-8')
                    fobj.write(VERSION)
                    fobj.close()
            except:
                pass

        # distutils uses old-style classes, so no super()
        build_py.run(self)


install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'urwid==1.3.1',
    'six']

setup(name='boksh',
      version=VERSION,
      description="Shell bookmarking application",
      long_description=README + '\n\n' + NEWS,
      cmdclass={'build_py': my_build_py},
      classifiers=[
          # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3"],
      keywords='ssh bookmark',
      author='Thomas Chiroux',
      author_email='',
      url='https://github.com/ThomasChiroux/boksh',
      license='GPLv3',
      entry_points={
          'console_scripts': ['boksh = boksh.commands:main', ],
      },
      packages=find_packages(),
      package_data={'': ['RELEASE-VERSION', '*.rst', '*.json', ]},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      #test_suite = 'test.run_all_tests.run_all_tests',
      tests_require=['nose', 'coverage', 'unittest2'],
      test_suite='nose.collector',
      extras_require={
          'doc':  ["sphinx", ],
      },)

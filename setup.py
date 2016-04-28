#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu Apr 16 16:39:01 CEST 2015
#
# Copyright (C) 2011-2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

setup(

    name='bob.db.cuhk_cufs',
    version=version,
    description='CUHK Face Sketch Database (CUFS)',
    url='',
    license='BSD',
    keywords = "",
    author='Tiago de Freitas Pereira',
    author_email='tiago.pereira@idiap.ch',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,

    install_requires=[
      'setuptools',
      'bob.db.xm2vts',
      'bob.db.arface',
      'bob.db.verification.utils' 
    ],

    namespace_packages = [
      'bob',
      'bob.db',
    ],

    entry_points = {
      # declare database to bob
      'bob.db': [
        'cuhk_cufs = bob.db.cuhk_cufs.driver:Interface',
      ],
      
      # scripts should be declared using this entry:
      'console_scripts' : [
        'evaluate_cufs.py = bob.db.cuhk_cufs.scripts.evaluate_cufs:main',
        'html_report.py   = bob.db.cuhk_cufs.scripts.html_report:main',
      ],      
      
    },

    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Education',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
    ],
)

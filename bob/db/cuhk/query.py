#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Tue Aug 14 14:28:00 CEST 2015
#
# Copyright (C) 2012-2014 Idiap Research Institute, Martigny, Switzerland
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

import os
import six
from bob.db.base import utils
from .models import *
from .driver import Interface

import bob.db.verification.utils

SQLITE_FILE = Interface().files()[0]

class Database(bob.db.verification.utils.SQLiteDatabase, bob.db.verification.utils.ZTDatabase):

  """Wrapper class for the CUHK-CUFS database for Heterogeneous face recognition recognition (http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html).

  """

  def __init__(self, original_directory = None, original_extension = None, annotation_directory = None):
    # call base class constructors to open a session to the database
    bob.db.verification.utils.SQLiteDatabase.__init__(self, SQLITE_FILE, File)
    bob.db.verification.utils.ZTDatabase.__init__(self, original_directory=original_directory, original_extension=original_extension)


  def objects(self, groups = None, protocol = None, purposes = None, model_ids = None, **kwargs):
    """This function returns lists of File objects, which fulfill the given restrictions."""


  def model_ids(self, protocol=None, groups=None, gender=None):
    return []


  def groups(self, protocol = None, **kwargs):
    """This function returns the list of groups for this database."""


  def tmodel_ids(self, groups = None, protocol = None, **kwargs):
    """This function returns the ids of the T-Norm models of the given groups for the given protocol."""


  def tobjects(self, protocol=None, model_ids=None, groups=None):
    #No TObjects    
    return []


  def zobjects(self, protocol=None, groups=None):
    #No TObjects    
    return []


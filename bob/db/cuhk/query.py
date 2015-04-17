#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu Oct 09 11:27:27 CEST 2014
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

import bob.db.verification.filelist

class Database(bob.db.verification.filelist.Database):
  """Wrapper class for the CASIA NIR-VIS 2.0 database for face recognition recognition (http://www.cbsr.ia.ac.cn/english/NIR-VIS-2.0-Database.html).
  this class defines a simple protocol for training, dev and and by splitting the audio files of the database in three main parts.
  """

  def __init__(self, original_directory = None, original_extension = None, annotation_directory=None):
    # call base class constructor
    from pkg_resources import resource_filename
    lists = resource_filename(__name__, 'lists')
    bob.db.verification.filelist.Database.__init__(self, lists, original_directory = original_directory, original_extension = original_extension, annotation_directory=annotation_directory)


  def tobjects(self, protocol=None, model_ids=None, groups=None):
    #No TObjects    
    return []


  def zobjects(self, protocol=None, groups=None):
    #No TObjects    
    return []


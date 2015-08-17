#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira<tiago.pereira@idiap.ch>
# @date:   Mon Aug  9 14:12:51 CEST 2015
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Table models and functionality for the CUHK-CUFS DATABASE

This model, models only the CUHK part.
The ARFACE part and the XM2VTS part are extended from, respectivelly, bob.db.arface, bob.db.xm2vts

"""

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, or_, and_, not_
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import bob.db.verification.utils

import os

Base = declarative_base()

""" Defining protocols. Yes, they are static """
PROTOCOLS = ('cuhk_p2s', 'arface_p2s', 'xm2vts_p2s', 'all-mixed_p2s', 'cuhk-arface-xm2vts_p2s', 'cuhk-xm2vts-arface_p2s',
  'arface-cuhk-xm2vts_p2s', 'arface-xm2vts-cuhk_p2s', 'xm2vts-cuhk-arface_p2s', 'xm2vts-arface-cuhk_p2s',
  'cuhk_s2p', 'arface_s2p', 'xm2vts_s2p', 'all-mixed_s2p', 'cuhk-arface-xm2vts_s2p', 'cuhk-xm2vts-arface_s2p',
  'arface-cuhk-xm2vts_s2p', 'arface-xm2vts-cuhk_s2p', 'xm2vts-cuhk-arface_s2p', 'xm2vts-arface-cuhk_s2p')


GROUPS    = ('world', 'dev', 'eval')

PURPOSES   = ('train', 'enroll', 'probe')


class Protocol_File_Association(Base):
  """
  Describe the protocols
  """
  __tablename__ = 'protocol_file_association'

  protocol = Column('protocol', Enum(*PROTOCOLS), primary_key=True)
  group    = Column('group', Enum(*GROUPS), primary_key=True)
  purpose  = Column('purpose', Enum(*PURPOSES), primary_key=True)
  file_id  = Column('file_id',  Integer, ForeignKey('file.id'), primary_key=True)

  def __init__(self, protocol, group, purpose, file_id):
    self.protocol = protocol
    self.group    = group
    self.purpose  = purpose
    self.file_id  = file_id



class Client(Base):
  """
  Information about the clients (identities) of the CUHK-CUFS.

  """
  __tablename__ = 'client'

  # We define the possible values for the member variables as STATIC class variables
  gender_choices    = ('man', 'woman','none')
  database_choices  = ('cuhk','arface','xm2vts') 

  id          = Column(Integer, primary_key=True)
  original_id       = Column(Integer)
  original_database = Column(Enum(*database_choices))
  gender = Column(Enum(*gender_choices))

  def __init__(self, id, gender, original_id, original_database):
    self.id = id
    self.gender = gender
    self.original_id = original_id
    self.original_database = original_database

  def __repr__(self):
    return "<Client({0}, {1}, {2})>".format(self.id, self.original_database, self.original_id)


class Annotation(Base):
  """
  The CUHK-CUFS provides 35 coordinates.
  To model this coordinates this table was built.
  The columns are the following:

    - Annotation.id
    - x
    - y

  """  
  __tablename__ = 'annotation'

  file_id = Column(Integer, ForeignKey('file.id'), primary_key=True)
  x     = Column(Integer, primary_key=True)
  y     = Column(Integer, primary_key=True)  
  index = Column(Integer) 

  def __init__(self, file_id, x,y, index=0):
    self.file_id = file_id
    self.x          = x
    self.y          = y
    self.index      = index


  def __repr__(self):
    return "<Annotation(file_id:{0}, index:{1}, y={2}, x={3})>".format(self.file_id, self.index, self.y, self.x)



class File(Base, bob.db.verification.utils.File):
  """
  Information about the files of the CUHK-CUFS database.

  Each file includes
  * the client id
  """
  __tablename__ = 'file'

  modality_choices = ('photo', 'sketch')

  id        = Column(String(100), primary_key=True, autoincrement=True)
  path      = Column(String(100), unique=True)
  client_id = Column(Integer, ForeignKey('client.id'))
  modality  = Column(Enum(*modality_choices))

  # a back-reference from the client class to a list of files
  client      = relationship("Client", backref=backref("files", order_by=id))
  all_annotations = relationship("Annotation", backref=backref("file"), uselist=True, order_by=Annotation.index)

  def __init__(self, id, image_name, client_id, modality):
    # call base class constructor
    bob.db.verification.utils.File.__init__(self, file_id = id, client_id = client_id, path = image_name)
    #bob.db.verification.utils.File.__init__(self, client_id = client_id, path = image_name)
    self.modality = modality

  def annotations(self, annotation_type="eyes_center"):
    if annotation_type=="eyes_center":
      return {'reye' : (self.all_annotations[16].y, self.all_annotations[16].x), 'leye' : (self.all_annotations[18].y, self.all_annotations[18].x) }
    else:      
      data = {}
      for i in range(len(self.all_annotations)):
        a = self.all_annotations[i]
        data[i] = (a.y, a.x)
 
      return data

    




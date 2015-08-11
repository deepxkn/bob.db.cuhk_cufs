#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# @date:   Tue Aug  11 14:07:00 CEST 2015
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
This script creates the CUHK-CUFS database in a single pass.
"""

import os

from .models import *
from utils import ARFACEWrapper, XM2VTSWrapper, CUHKWrapper

def add_clients(session, verbose = True):

  """Adds the clients and split up the groups 'world', 'dev', and 'eval'"""

  #import ipdb; ipdb.set_trace();
   
  #Adding the clients from ARFACE
  arface_clients = ARFACEWrapper.get_clients()

  if verbose>=1: print('Adding ARFACE clients to the database ...')
    
  client_ids = range(1,len(arface_clients)+1)
  id_offset = 1
  for id in client_ids:
    id_offset = id
    original_client_id = arface_clients[id-1]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id, 
                       gender=ARFACEWrapper.get_gender_from_client_id(original_client_id),
                       original_id = original_client_id,
                       original_database = "arface"
                       ))
  del arface_clients


  #Adding the clients from XM2VTS
  xm2vts_clients = XM2VTSWrapper.get_clients()

  if verbose>=1: print('Adding XM2VTS clients to the database ...')
    
  client_ids = range(len(xm2vts_clients))
  for id in client_ids:
    id_offset += 1
    original_client_id = xm2vts_clients[id]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id_offset, 
                       gender=XM2VTSWrapper.get_gender(),
                       original_id = original_client_id,
                       original_database = "xm2vts"
                       ))
  del xm2vts_clients


  #Adding the clients from CUHK
  cuhk_clients = CUHKWrapper.get_clients()

  if verbose>=1: print('Adding CUHK clients to the database ...')
    
  client_ids = range(len(cuhk_clients))
  for id in client_ids:
    id_offset += 1
    original_client_id = cuhk_clients[id-1]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id_offset, 
                       gender=CUHKWrapper.get_gender_from_client_id(original_client_id),
                       original_id = original_client_id,
                       original_database = "cuhk"
                       ))

  if verbose>=1: print("Commiting changes of clients to db") 
  del cuhk_clients

  session.commit();




def add_files(session, directory, annotations_file, verbose):
  """
  Adds files with their respective information into the Database
  :param session: DB session
  :param directory: directory to the CASME2 directory containing the folders of subjects.
  :param annotations_file: annotations for the dataset file path
  :param verbose: whether or not to show some information on CLI
  """
  return None



def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2));
  Client.metadata.create_all(engine)
  File.metadata.create_all(engine) 
  Annotation.metadata.create_all(engine)
  

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
  add_clients(s, args.verbose)
  #add_files(s, args.directory, args.annotdir, args.verbose)
  #add_protocols(s, args.verbose)
  #add_clientxprotocols(s, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way?')
  parser.add_argument('-D', '--directory', metavar='DIR', default='../CASME2/Cropped/', help='The path to the directory containing the subjects folders, which have the frames')
  parser.add_argument('--extension', metavar='STR', default='.jpg', help='The file extension of the image files from the CASME2 database')
  parser.add_argument('-A', '--annotdir', metavar='DIR', default='bob/db/casme2/annotations.csv', help="Change the relative path to the directory containing the action_unit information file of the CASME2 database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action

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
   
  #Adding the clients from ARFACE
  arface = ARFACEWrapper()
  arface_clients = arface.get_clients()

  if verbose>=1: print('Adding ARFACE clients to the database ...')
    
  client_ids = range(1,len(arface_clients)+1)
  id_offset = 1
  for id in client_ids:
    id_offset = id
    original_client_id = arface_clients[id-1]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id, 
                       gender = arface.get_gender_from_client_id(original_client_id),
                       original_id = original_client_id,
                       original_database = "arface"
                       ))
  del arface_clients


  #Adding the clients from XM2VTS
  xm2vts = XM2VTSWrapper()
  xm2vts_clients = xm2vts.get_clients()

  if verbose>=1: print('Adding XM2VTS clients to the database ...')
    
  client_ids = range(len(xm2vts_clients))
  for id in client_ids:
    id_offset += 1
    original_client_id = xm2vts_clients[id]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id_offset, 
                       gender=xm2vts.get_gender(),
                       original_id = original_client_id,
                       original_database = "xm2vts"
                       ))
  del xm2vts_clients


  #Adding the clients from CUHK
  cuhk         = CUHKWrapper()
  cuhk_clients = cuhk.get_clients()

  if verbose>=1: print('Adding CUHK clients to the database ...')
    
  client_ids = range(len(cuhk_clients))
  for id in client_ids:
    id_offset += 1
    original_client_id = cuhk_clients[id-1]
 
    if verbose>=1: print("  Adding client {0}".format(original_client_id))   
    session.add(Client(id=id_offset, 
                       gender=cuhk.get_gender_from_client_id(original_client_id),
                       original_id = original_client_id,
                       original_database = "cuhk"
                       ))

  if verbose>=1: print("Commiting changes of clients to db") 
  del cuhk_clients

  session.commit();



def add_files(session, verbose):
  """
  Adds files with their respective information into the Database
  """
  if verbose>=1: print('Adding ARFACE files to the database ...')
  if verbose>=1: print('Adding PHOTOS ...')
  
  arface = ARFACEWrapper()
  files = arface.get_files_from_modality(modality='photo')
  id_offset = 1 #ID
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)


  if verbose>=1: print('Adding SKETCHES ...') 
  files = arface.get_files_from_modality(modality='sketches')    
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)

  del arface

  ########

  if verbose>=1: print('Adding XM2VTS files to the database ...')
  if verbose>=1: print('Adding PHOTOS ...')
 
  xm2vts = XM2VTSWrapper()
  files = xm2vts.get_files_from_modality(modality='photo')
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)


  if verbose>=1: print('Adding SKETCHES ...') 
  files = xm2vts.get_files_from_modality(modality='sketches')    
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)

  #######

  if verbose>=1: print('Adding CUHK files to the database ...')
 
  cuhk = CUHKWrapper()
  files = cuhk.get_files()
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)


  
  session.commit()


def add_annotations(session, annotation_dir, verbose):
  """
  Adds the annotations 
  """

  if verbose>=1: print('Adding ARFACE Annotations to the database ...')
  arface = ARFACEWrapper()
  annotations = arface.get_annotations(annotation_dir, annotation_extension='.dat')
  for a in annotations:
    session.add(a)

  if verbose>=1: print('Adding XM2VTS Annotations to the database ...')
  xm2vts = XM2VTSWrapper()
  annotations = xm2vts.get_annotations(annotation_dir, annotation_extension='.dat')
  for a in annotations:
    session.add(a)

  if verbose>=1: print('Adding CUHK Annotations to the database ...')
  cuhk = CUHKWrapper()
  annotations = cuhk.get_annotations(annotation_dir, annotation_extension='.dat')
  for a in annotations:
    session.add(a)

  session.commit()   



def add_protocols(session, verbose, photo2sketch=True):
  """
  There are 9 protocols:
 
  CUHK   - This covers only images from the CUHK student database
  ARFACE - This covers only images from the ARFACE  database
  XM2VTS - This covers only images from the XM2VTS student database
  
  ALL    - It is a mixture of all databases (the training, dev and eval sets of all)

  CUHK-ARFACE-XM2VTS: Training set of CUHK, dev set of ARFACE and eval set of XM2VTS
  CUHK-XM2VTS-ARFACE:
  ARFACE-CUHK-XM2VTS:
  ARFACE-XM2VTS-CUHK:
  XM2VTS-CUHK-ARFACE:
  XM2VTS-ARFACE-CUHK:

  """

  PROTOCOLS = ('cuhk_p2s', 'arface_p2s', 'xm2vts_p2s', 'all-mixed_p2s', 'cuhk-arface-xm2vts_p2s', 'cuhk-xm2vts-arface_p2s',
  'arface-cuhk-xm2vts_p2s', 'arface-xm2vts-cuhk_p2s', 'xm2vts-cuhk-arface_p2s', 'xm2vts-arface-cuhk_p2s',
  'cuhk_s2p', 'arface_s2p', 'xm2vts_s2p', 'all-mixed_s2p', 'cuhk-arface-xm2vts_s2p', 'cuhk-xm2vts-arface_s2p',
  'arface-cuhk-xm2vts_s2p', 'arface-xm2vts-cuhk_s2p', 'xm2vts-cuhk-arface_s2p', 'xm2vts-arface-cuhk_s2p')

  GROUPS    = ('world', 'dev', 'eval')

  PURPOSES   = ('train', 'enrol', 'probe')

  arface = ARFACEWrapper()
  xm2vts = XM2VTSWrapper()
  cuhk   = CUHKWrapper()

  if(photo2sketch):
    suffix = "_p2s"
  else:
    suffix = "_s2p"    

  ####### Protocol ARFACE

  if verbose>=1: print('Creating the protocol ARFACE  ...')

  #getting the files
  world_files = arface.get_files_from_group(group="world")
  dev_files   = arface.get_files_from_group(group="dev")
  eval_files  = arface.get_files_from_group(group="eval")
  
  #Inserting in the database
  insert_protocol_data(session, "arface"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()

  
  ############## Protocol XM2VTS
  if verbose>=1: print('Creating the protocol XM2VTS  ...')

  #getting the files
  world_files = xm2vts.get_files_from_group(group="world")
  dev_files   = xm2vts.get_files_from_group(group="dev")
  eval_files  = xm2vts.get_files_from_group(group="eval")
 
  #Inserting in the database
  insert_protocol_data(session, "xm2vts"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()



  ############## Protocol CUHK

  if verbose>=1: print('Creating the protocol CUHK  ...')

  #getting the files
  world_files = cuhk.get_files_from_group(group="world")
  dev_files   = cuhk.get_files_from_group(group="dev")
  eval_files  = cuhk.get_files_from_group(group="eval")
 
  #Inserting in the database
  insert_protocol_data(session, "cuhk"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol all-mixed

  if verbose>=1: print('Creating the protocol ALL mixed  ...')

  #getting the files
  world_files = arface.get_files_from_group(group="world") +\
                xm2vts.get_files_from_group(group="world") +\
                cuhk.get_files_from_group(group="world")

  dev_files   = arface.get_files_from_group(group="dev") +\
                xm2vts.get_files_from_group(group="dev") +\
                cuhk.get_files_from_group(group="dev")

  eval_files  = arface.get_files_from_group(group="eval") +\
                xm2vts.get_files_from_group(group="eval") +\
                cuhk.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "all-mixed"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "all-mixed"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "all-mixed"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol cuhk-arface-xm2vts

  if verbose>=1: print('Creating the protocol cuhk-arface-xm2vts  ...')

  #getting the files
  world_files = cuhk.get_files_from_group(group="world")
  dev_files   = arface.get_files_from_group(group="dev")
  eval_files  = xm2vts.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "cuhk-arface-xm2vts"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk-arface-xm2vts"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk-arface-xm2vts"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol cuhk-xm2vts-arface

  if verbose>=1: print('Creating the protocol cuhk-xm2vts-arface  ...')

  #getting the files
  world_files = cuhk.get_files_from_group(group="world")
  dev_files   = xm2vts.get_files_from_group(group="dev")
  eval_files  = arface.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "cuhk-xm2vts-arface"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk-xm2vts-arface"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "cuhk-xm2vts-arface"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol arface-cuhk-xm2vts 

  if verbose>=1: print('Creating the protocol arface-cuhk-xm2vts  ...')

  #getting the files
  world_files = arface.get_files_from_group(group="world")
  dev_files   = cuhk.get_files_from_group(group="dev")
  eval_files  = xm2vts.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "arface-cuhk-xm2vts"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface-cuhk-xm2vts"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface-cuhk-xm2vts"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol arface-xm2vts-cuhk

  if verbose>=1: print('Creating the protocol arface-xm2vts-cuhk  ...')

  #getting the files
  world_files = arface.get_files_from_group(group="world")
  dev_files   = xm2vts.get_files_from_group(group="dev")
  eval_files  = cuhk.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "arface-xm2vts-cuhk"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface-xm2vts-cuhk"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "arface-xm2vts-cuhk"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()


  ############# Protocol xm2vts-cuhk-arface

  if verbose>=1: print('Creating the protocol xm2vts-cuhk-arface  ...')

  #getting the files
  world_files = xm2vts.get_files_from_group(group="world")
  dev_files   = cuhk.get_files_from_group(group="dev")
  eval_files  = arface.get_files_from_group(group="eval")

 
  #Inserting in the database
  insert_protocol_data(session, "xm2vts-cuhk-arface"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts-cuhk-arface"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts-cuhk-arface"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()



  ############# Protocol xm2vts-arface-cuhk

  if verbose>=1: print('Creating the protocol xm2vts-arface-cuhk  ...')

  #getting the files
  world_files = xm2vts.get_files_from_group(group="world")
  dev_files   = arface.get_files_from_group(group="dev")
  eval_files  = cuhk.get_files_from_group(group="eval")
 
  #Inserting in the database
  insert_protocol_data(session, "xm2vts-arface-cuhk"+suffix, "world", "train", world_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts-arface-cuhk"+suffix, "dev", "", dev_files, photo2sketch=photo2sketch)
  insert_protocol_data(session, "xm2vts-arface-cuhk"+suffix, "eval", "", eval_files, photo2sketch=photo2sketch)

  session.commit()




def insert_protocol_data(session, protocol, group, purpose, file_objects, photo2sketch=True):

  for f in file_objects:
    if purpose!="train":
      if photo2sketch and f.modality=="photo":
        purpose = "enrol"
      else:
        purpose = "probe"
     
    session.add(bob.db.cuhk.Protocol_File_Association(
       protocol, group, purpose, f.id))
 


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
  add_files(s, args.verbose)
  add_annotations(s, args.annotation_dir, args.verbose)

  add_protocols(s, args.verbose,photo2sketch=True)
  add_protocols(s, args.verbose,photo2sketch=False)

  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
  parser.add_argument('-a', '--annotation-dir', default='.',  help="The annotation directory. HAS TO BE THE SAME STRUCTURE AS PROVIDED BY THE DATABASE PROVIDERS (defaults to %(default)s)")

  parser.set_defaults(func=create) #action

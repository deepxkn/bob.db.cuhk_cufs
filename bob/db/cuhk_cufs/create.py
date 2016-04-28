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
from .utils import ARFACEWrapper, XM2VTSWrapper, CUHKWrapper
import numpy
numpy.random.seed(10)

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
   
  ############
  #Amendment: Creating a structure to make easy the protocol creation
  ############  
  client_files = {}
  client_files['arface'] = {}
  client_files['xm2vts'] = {}
  client_files['cuhk']   = {}  
  
  

  arface = ARFACEWrapper()
  files = arface.get_files_from_modality(modality='photo')
  id_offset = 1 #ID  
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1

    client_files['arface'][f.client_id] = {'photo':f.id}
    
    session.add(f)


  if verbose>=1: print('Adding SKETCHES ...') 
  files = arface.get_files_from_modality(modality='sketches')    
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    session.add(f)    
    client_files['arface'][f.client_id]['sketch'] = f.id

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
    client_files['xm2vts'][f.client_id] = {'photo':f.id}
    session.add(f)


  if verbose>=1: print('Adding SKETCHES ...') 
  files = xm2vts.get_files_from_modality(modality='sketches')    
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
    client_files['xm2vts'][f.client_id]['sketch'] = f.id
    session.add(f)

  #######

  if verbose>=1: print('Adding CUHK files to the database ...')
 
  cuhk = CUHKWrapper()
  files = cuhk.get_files()
  for f in files:
    if verbose>=1: print("  Adding file {0}".format(f.path))
    f.id = id_offset
    id_offset+=1
 
    if(not client_files['cuhk'].has_key(f.client_id)):
      client_files['cuhk'][f.client_id] = {}    
    client_files['cuhk'][f.client_id][f.modality] = f.id
    
    session.add(f)
  
  session.commit()
  
  return client_files


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




def add_search_protocols(session, verbose, clients_files):
  """
  Implementing the search protocols based on the paper
  
  Klare, Brendan F., and Anil K. Jain. "Heterogeneous face recognition using kernel prototype similarities." Pattern Analysis and Machine Intelligence, IEEE Transactions on 35.6 (2013): 1410-1422.

  In this one: 404 clients for training
               202 clients for testing
  """
  
  protocols = ['search_split1','search_split2','search_split3','search_split4','search_split5']
  
  clients = dict(clients_files['arface'].items() + clients_files['xm2vts'].items() + clients_files['cuhk'].items())
  
  for p in protocols:

    indexes = clients.keys()
    numpy.random.shuffle(indexes) #Shufling the indexes
  
    world   = indexes[0:404]
    dev     = indexes[404:404+202]
  
    if verbose>=1: print("  Adding protocol {0}".format(p)) 
  
    #Adding training set
    for w in world:

      for f in clients[w]:
      

        #ADDING PHOTO -> SKETCH
        protocol = "{0}_p2s".format(p)
        session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                    protocol,
                    "world",
                    "train", 
                    clients[w][f]))

        #ADDING PHOTO <- SKETCH
        protocol = "{0}_s2p".format(p)        
        session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                    protocol,
                    "world",
                    "train", 
                    clients[w][f]))


    #Adding dev set    
    for d in dev:
      
      #ADDING PHOTO -> SKETCH 
      # ENROLL
      protocol = "{0}_p2s".format(p)
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "dev",
                  "enroll", 
                  clients[d]['photo']))

      #ADDING PHOTO -> SKETCH
      # PROBE
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                    protocol,
                    "dev",
                    "probe", 
                    clients[d]['sketch']))



      #ADDING PHOTO <- SKETCH 
      # ENROLL
      protocol = "{0}_s2p".format(p)
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "dev",
                  "enroll", 
                  clients[d]['sketch']))

      #ADDING PHOTO <- SKETCH
      # PROBE
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                    protocol,
                    "dev",
                    "probe", 
                    clients[d]['photo']))






def add_verification_protocols(session, verbose, clients, protocol_name, n_train, n_dev, n_test):
  """
  Implementing verification protocols
  
  For the CUHK:    75 clients for training
                   56 clients for development
                   57 clients for testing
   
  
  For the XM2VTS:  118 clients for training
                   88 clients for development
                   89 clients for testing
  

  For the ARFACE:  44 clients for training
                   40 clients for development
                   39 clients for testing

  
  """  



  indexes = clients.keys()
  numpy.random.shuffle(indexes) #Shufling the indexes
  
  world    = indexes[0:n_train]
  dev      = indexes[n_train:n_train+n_dev]
  eval_set = indexes[n_train+n_dev:n_train+n_dev+n_test]
  
  if verbose>=1: print("  Adding protocol {0}".format(protocol_name)) 
  
  #Adding training set
  for w in world:

    for f in clients[w]:
      

      #ADDING PHOTO -> SKETCH
      protocol = "{0}_p2s".format(protocol_name)
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "world",
                  "train", 
                  clients[w][f]))

      #ADDING PHOTO <- SKETCH
      protocol = "{0}_s2p".format(protocol_name)        
      session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "world",
                  "train", 
                  clients[w][f]))



  #Adding dev set    
  for d in dev:
      
    #ADDING PHOTO -> SKETCH 
    # ENROLL
    protocol = "{0}_p2s".format(protocol_name)
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                protocol,
                "dev",
                "enroll", 
                clients[d]['photo']))

    #ADDING PHOTO -> SKETCH
    # PROBE
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                    protocol,
                    "dev",
                    "probe", 
                    clients[d]['sketch']))



    #ADDING PHOTO <- SKETCH 
    # ENROLL
    protocol = "{0}_s2p".format(protocol_name)
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                protocol,
                "dev",
                "enroll", 
                clients[d]['sketch']))

    #ADDING PHOTO <- SKETCH
    # PROBE
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "dev",
                  "probe", 
                  clients[d]['photo']))




  #Adding eval set    
  for e in eval_set:
      
    #ADDING PHOTO -> SKETCH 
    # ENROLL
    protocol = "{0}_p2s".format(protocol_name)
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                protocol,
                "eval",
                "enroll", 
                clients[e]['photo']))

    #ADDING PHOTO -> SKETCH
    # PROBE
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "eval",
                  "probe", 
                  clients[e]['sketch']))



    #ADDING PHOTO <- SKETCH 
    # ENROLL
    protocol = "{0}_s2p".format(protocol_name)
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                protocol,
                "eval",
                "enroll", 
                clients[e]['sketch']))

    #ADDING PHOTO <- SKETCH
    # PROBE
    session.add(bob.db.cuhk_cufs.Protocol_File_Association(
                  protocol,
                  "eval",
                  "probe", 
                  clients[e]['photo']))



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
  client_files = add_files(s, args.verbose)
  
  add_annotations(s, args.annotation_dir, args.verbose)

  add_search_protocols(s, args.verbose, client_files)

  add_verification_protocols(s, args.verbose, 
                          client_files['arface'], 
                          protocol_name="arface", 
                          n_train = 44, 
                          n_dev   = 40, 
                          n_test  = 39)
  
  add_verification_protocols(s, args.verbose, 
                          client_files['xm2vts'], 
                          protocol_name="xm2vts", 
                          n_train = 118, 
                          n_dev   = 88, 
                          n_test  = 89)

  add_verification_protocols(s, args.verbose, 
                          client_files['cuhk'], 
                          protocol_name="cuhk", 
                          n_train = 75, 
                          n_dev   = 56, 
                          n_test  = 57)

  add_verification_protocols(s, args.verbose, 
                          dict(client_files['cuhk'].items() + client_files['arface'].items() + client_files['xm2vts'].items()), 
                          protocol_name="all-mixed", 
                          n_train = 237, 
                          n_dev   = 184, 
                          n_test  = 185)

  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
  parser.add_argument('-a', '--annotation-dir', default='.',  help="The annotation directory. HAS TO BE THE SAME STRUCTURE AS PROVIDED BY THE DATABASE PROVIDERS (defaults to %(default)s)")

  parser.set_defaults(func=create) #action

#!/usr/bin/env python 
# vim: set fileencoding=utf-8 : 
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch> 
# @date:   Tue Aug  11 17:08:00 CEST 2015 


"""
This file has some utilities to deal with the files provided by the database
"""

import os
class ARFACEWrapper():
  """
  Utility functions to deal with the AR Face database.
  """

  @staticmethod
  def get_clients(file_name=os.path.join(os.path.curdir,"bob","db","cuhk","AR_file_names_of_photos.txt")):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c[5:10])
    
    return clients

  @staticmethod 
  def get_gender_from_client_id(client_id):
    return 'man' if client_id[0]=='m' else 'woman'



class XM2VTSWrapper():
  """
  Utility functions to deal with the XM2VTS database.
  """

  @staticmethod
  def get_clients(file_name=os.path.join(os.path.curdir,"bob","db","cuhk","XM2VTS_file_names_of_photos.txt")):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c[5:8])
    
    return clients

  @staticmethod 
  def get_gender():
    return 'none'


class CUHKWrapper():
  """
  Utility functions to deal with the CUHK database.
  """

  @staticmethod
  def get_clients(file_name=os.path.join(os.path.curdir,"bob","db","cuhk","all-cuhk.lst")):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c.split(" ")[1].rstrip("\n"))
    
    return list(set(clients))

  @staticmethod 
  def get_gender_from_client_id(client_id):
    return 'man' if client_id[0]=='m' else 'woman'







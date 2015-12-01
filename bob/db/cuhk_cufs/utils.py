#!/usr/bin/env python 
# vim: set fileencoding=utf-8 : 
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch> 
# @date:   Tue Aug  11 17:08:00 CEST 2015 


"""
This file has some utilities to deal with the files provided by the database
"""

import os
import numpy
numpy.random.seed(10)
import bob.db.arface

def read_annotations(file_name):
  """
  Read the annotations in the format

  X Y\n
  X Y\n
  .
  .
  .
  """
  original_annotations = open(file_name).readlines()
  annotations         = []
  
  for a in original_annotations:
    a = a.rstrip("\n").rstrip("\r")
    data = a.split(" ")
    if(len(data)!=2): #NEED TO HAVE ONLY 2 COORDINATES
      continue
    else:
      annotations.append(data)

  return annotations


class ARFACEWrapper():
  """
  Utility functions to deal with the AR Face database.
  """

  def __init__(self, 
      photo_file_name=os.path.join(os.path.curdir,"bob","db","cuhk_cufs","data","AR_file_names_of_photos.txt"),
      sketch_file_name=os.path.join(os.path.curdir,"bob","db","cuhk_cufs","data","AR_file_names_of_sketches.txt")
   ):

    self.m_photo_file_name  = photo_file_name
    self.m_sketch_file_name = sketch_file_name


  def get_clients(self):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(self.m_photo_file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c[5:10])
    
    return clients

  
  def get_gender_from_client_id(self,client_id):
    return 'man' if client_id[0]=='m' else 'woman'


  def get_annotations(self, annotation_dir, annotation_extension='.dat'):
    """
    Get the annotation objects
    """

    db = bob.db.cuhk_cufs.Database()
    annotations = []
 
    for o in db.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_database=="arface"):
      #making the path
      if(o.modality=="sketch"):
        path = os.path.join(annotation_dir, o.path) + annotation_extension
      else:
        path = os.path.join(annotation_dir,"ARFACE", "photo", o.path) + annotation_extension

      #Reading the annotation file
      original_annotations = read_annotations(path)
      index = 0
      for a in original_annotations:
        
        annotations.append(bob.db.cuhk_cufs.Annotation(o.id, 
                                                  a[0],
                                                  a[1],
                                                  index = index
                                                 ))
        index += 1
    return annotations


  def get_files_from_modality(self, modality):
    """
    For a given modality, get the correct file object.

    If modality=='photo', all the information will be taken from bob.db.arface
    else, the data will be read from the original data files

    **Parameters**

      modality: Modality (photo | sketch)

      clients: The list of bob.db.cuhk_cufs.clients

    """

    files = []
    if(modality=='photo'):
      db = bob.db.arface.Database()
      
      #Parsing the provided data
      raw_files = open(self.m_photo_file_name).readlines()
      original_files = []      
      for f in raw_files:
        original_files.append(f[5:12])

      #Searching in the original database
      original_files = db.files(ids=original_files)
      for f in original_files:
        #self, id, image_name, client_id, modality        
        client = bob.db.cuhk_cufs.Database().query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id == f.id[0:5])
        assert client.count() == 1
        client = client[0]
        files.append(bob.db.cuhk_cufs.File(id = 0,
                                      client_id=client.id,
                                      image_name=f.path,
                                      modality = 'photo'
                                      )
                                     )
 

    else:
      #Parsing the provided data
      raw_files = open(self.m_sketch_file_name).readlines()
      for f in raw_files:
        f = f.rstrip("\n")
        original_client_id = f[0] + f[2:6] #the original client id is [m|w]-number
        client = bob.db.cuhk_cufs.Database().query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id == original_client_id.lower()) #GEtting the client_id
        assert client.count() == 1
        client = client[0]

        f = os.path.join("ARFACE","sketch",f)
        files.append(bob.db.cuhk_cufs.File(id         = 0,
                                      client_id  = client.id,
                                      image_name = f,
                                      modality   = 'sketch'
                                      )
                                     )

    return files    



class XM2VTSWrapper():
  """
  Utility functions to deal with the XM2VTS database.
  """

  def __init__(self, 
      photo_file_name=os.path.join(os.path.curdir,"bob","db","cuhk_cufs","data","XM2VTS_file_names_of_photos.txt"),
      sketch_file_name=os.path.join(os.path.curdir,"bob","db","cuhk_cufs","data","XM2VTS_file_names_of_sketches.txt")
   ):

    self.m_photo_file_name  = photo_file_name
    self.m_sketch_file_name = sketch_file_name



  def get_clients(self):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(self.m_photo_file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c[5:8])
    
    return clients

  def get_gender(self):
    return 'none'



  def get_annotations(self, annotation_dir, annotation_extension='.dat'):
    """
    Get the annotation objects
    """

    db = bob.db.cuhk_cufs.Database()
    annotations = []
 
    for o in db.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_database=="xm2vts"):
      #making the path
      if(o.modality=="sketch"):
        path = os.path.join(annotation_dir, o.path) + annotation_extension
      else:
        file_name = o.path.split("/")[2] #THE ORIGINAL XM2VTS RELATIVE PATH IS: XXX\XXX\XXX
        path = os.path.join(annotation_dir,"xm2vts", "photo", file_name) + "_f02" +  annotation_extension #FOR SOME REASON THE AUTHORS SET THIS '_f02 IN THE END OF THE FILE'

      #Reading the annotation file
      original_annotations = read_annotations(path)
      index = 0
      for a in original_annotations:
        
        annotations.append(bob.db.cuhk_cufs.Annotation(o.id, 
                                                  a[0],
                                                  a[1],
                                                  index = index
                                                 ))
        index += 1
    return annotations




  def get_files_from_modality(self, modality):
    """
    For a given modality, get the correct file object.

    If modality=='photo', all the information will be taken from bob.db.arface
    else, the data will be read from the original data files

    **Parameters**

      modality: Modality (photo | sketch)

      clients: The list of bob.db.cuhk_cufs.clients

    """

    files = []
    if(modality=='photo'):
      db = bob.db.xm2vts.Database()
      
      #Parsing the provided data
      raw_files = open(self.m_photo_file_name).readlines()
      original_files = []      
      for f in raw_files:
        original_files.append(f[5:12])

      for f in original_files:
        #getting the original file object
        query = db.query(bob.db.xm2vts.File).filter(bob.db.xm2vts.File.path.endswith(f))
        assert query.count()==1
        f_obj = query[0] 

        #getting the CUHK-CUFS file
        client = bob.db.cuhk_cufs.Database().query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id == f[0:3])
        assert client.count() == 1
        client = client[0]
 
        files.append(bob.db.cuhk_cufs.File(id = 0,
                                      client_id=client.id,
                                      image_name=f_obj.path,
                                      modality = 'photo'
                                      )
                                     )
 
    else:
      #Parsing the provided data
      raw_files = open(self.m_sketch_file_name).readlines()

      for f in raw_files:
        f = f.rstrip("\n")
        original_client_id = str(int(f[0:3]))        
        client = bob.db.cuhk_cufs.Database().query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id == original_client_id)
        assert client.count() == 1
        client = client[0]

        f = os.path.join("xm2vts","sketch",f) 
        files.append(bob.db.cuhk_cufs.File(id         = 0,
                                      client_id  = client.id,
                                      image_name = f,
                                      modality   = 'sketch'
                                      )
                                     )

    return files    





class CUHKWrapper():
  """
  Utility functions to deal with the CUHK database.
  """

  def __init__(self, 
      file_name=os.path.join(os.path.curdir,"bob","db","cuhk_cufs","data","all-cuhk.txt"),      
   ):

    self.m_file_name  = file_name


  def get_clients(self):
    """
    Basically read the input file and extract the clients from the original file_name
    """
    raw_clients = open(self.m_file_name).readlines()
    clients = []
    for c in raw_clients:
      clients.append(c.split(" ")[1].rstrip("\n"))
    
    return list(set(clients))


  def get_gender_from_client_id(self, client_id):
    return 'man' if client_id[0]=='m' else 'woman'



  def get_annotations(self, annotation_dir, annotation_extension='.dat'):
    """
    Get the annotation objects
    """

    db = bob.db.cuhk_cufs.Database()
    annotations = []
 
    for o in db.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_database=="cuhk"):
      #making the path
      path = os.path.join(annotation_dir, o.path) + annotation_extension

      #Reading the annotation file
      original_annotations = read_annotations(path)
      index = 0
      for a in original_annotations:
        annotations.append(bob.db.cuhk_cufs.Annotation(o.id, 
                                                  a[0],
                                                  a[1],
                                                  index = index
                                                 ))
        index += 1
 
    return annotations


  def get_files(self):
    """
    Get the correct file object from insert
    """
    raw_data = open(self.m_file_name).readlines()
    files = []
    for d in raw_data:
      d = d.rstrip("\n")

      original_client_id = d.split(" ")[1]
      image_name         = d.split(" ")[0]
      modality           = 'sketch' if (image_name.find('sketch')>-1) else 'photo'

      client = bob.db.cuhk_cufs.Database().query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id == original_client_id)
      assert client.count() == 1
      client = client[0]    

      files.append(bob.db.cuhk_cufs.File(id         = 0,
                                    client_id  = client.id,
                                    image_name = image_name,
                                    modality   = modality
                                    )
                                   )

    return files

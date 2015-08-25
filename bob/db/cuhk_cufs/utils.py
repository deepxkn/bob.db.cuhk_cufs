#!/usr/bin/env python 
# vim: set fileencoding=utf-8 : 
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch> 
# @date:   Tue Aug  11 17:08:00 CEST 2015 


"""
This file has some utilities to deal with the files provided by the database
"""

import os
import numpy
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


  def get_clients_from_group(self, group=""):
    """
    Get the bob.db.cuhk_cufs.File for a given group (world, dev or eval).

    Follow bellow the steps for this selection.

     1 - Select the bob.db.arface.Client for a given group
     2 - Search the correspondent bob.db.cuhk_cufs.File joint with bob.db.cuhk_cufs.Client using the original_client_id as a search criteria.
     3 - Accumulate the result of the search.
    """
    arface = bob.db.arface.Database()
    cuhk   = bob.db.cuhk_cufs.Database()
    import sqlalchemy

    #Getting the clients from ARFACE
    original_clients = arface.query(bob.db.arface.Client).filter(bob.db.arface.Client.sgroup==group)
    
    #Getting the correspondent files from bob.db.cuhk_cufs
    clients = []    
    for o in original_clients:
      cuhk_clients = cuhk.query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id==o.id).options(sqlalchemy.orm.subqueryload(bob.db.cuhk_cufs.Client.files)) #forcing to bring the clients
      for c in cuhk_clients:
        clients.append(c)

    return list(clients)


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

  def get_clients_from_group(self, group=""):
    """
    This is a hand made protocol since the XM2VTS database is biased.

    For that I shuffled the indexes of the 295 clients and will take:
      - 40% for training --> 118
      - 30% for developement --> 88
      - 30% for testing --> 89
    """
    
    indexes = [273, 241, 285, 256, 173, 193, 107, 55, 53, 143, 163, 63, 13, 113, 258, 271, 134, 17, 20, 227, 203, 96, 66, 112, 77, 237, 42, 61, 272, 161, 209, 206, 195, 140, 150, 294, 152, 136, 188, 232, 21, 75, 141, 25, 249, 269, 70, 217, 251, 29, 153, 83, 185, 94, 116, 265, 177, 38, 156, 191, 118, 121, 204, 100, 255, 286, 78, 260, 282, 33, 242, 200, 91, 224, 137, 180, 65, 12, 3, 151, 154, 1, 290, 198, 167, 212, 72, 133, 144, 57, 0, 211, 48, 292, 213, 277, 52, 223, 115, 230, 49, 4, 291, 214, 18, 71, 146, 289, 250, 268, 201, 170, 11, 178, 2, 155, 264, 64, 287, 14, 110, 30, 19, 149, 68, 183, 44, 60, 181, 283, 86, 139, 81, 126, 202, 120, 10, 9, 164, 218, 43, 148, 105, 186, 225, 93, 184, 50, 257, 132, 254, 27, 108, 106, 69, 252, 138, 122, 196, 175, 228, 7, 168, 135, 15, 231, 182, 280, 147, 54, 261, 79, 281, 125, 142, 101, 259, 41, 187, 16, 275, 248, 179, 169, 89, 245, 26, 73, 199, 90, 128, 236, 40, 166, 262, 84, 32, 97, 92, 174, 284, 37, 36, 111, 82, 104, 58, 98, 235, 215, 220, 130, 85, 216, 205, 274, 22, 244, 129, 247, 6, 240, 279, 5, 109, 31, 74, 127, 95, 117, 210, 165, 80, 59, 114, 194, 238, 207, 239, 267, 159, 243, 131, 171, 67, 222, 8, 47, 45, 99, 123, 229, 293, 270, 253, 46, 162, 263, 102, 76, 88, 28, 158, 278, 62, 246, 176, 124, 234, 276, 87, 24, 157, 119, 197, 190, 35, 34, 160, 56, 266, 172, 39, 233, 221, 192, 288, 23, 226, 219, 189, 208, 145, 103, 51]
   
    #Fetching the clients
    import sqlalchemy
    cuhk   = bob.db.cuhk_cufs.Database()
    all_clients = numpy.array(cuhk.query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_database=="xm2vts").order_by(bob.db.cuhk_cufs.Client.original_id).options(sqlalchemy.orm.subqueryload(bob.db.cuhk_cufs.Client.files)).all()) #forcing to bring the clients.

    data_training = 118
    data_dev      = 88
    data_eval     = 89

    clients = []
    if(group=="world"):
      offset = 0      
      clients = all_clients[indexes[offset:offset+data_training]]
    elif(group=="dev"):
      offset = data_training
      clients = all_clients[indexes[offset:offset+data_dev]]
    else: 
      offset  = data_training + data_dev
      clients = all_clients[indexes[offset:offset+data_eval]]
       
 
    #Fetching the correspondent files from bob.db.cuhk_cufs
    #files = []    
    #for c in clients:
      #cuhk_files = cuhk.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.id==c.id)
      #for f in cuhk_files:
        #files.append(f)

    return list(clients)
    

  def get_files_from_group_biased(self, group=""):
    """
    TODO: THE BOB.DB.XM2VTS PROTOCOLS ARE BIASED

    Get the bob.db.cuhk_cufs.File for a given group (world, dev or eval).

    There is no way to do it using ORM so I did a powerful SQL query in the XM2VTS.

    SELECT client.* FROM client 
      LEFT JOIN file ON file.client_id = client.id 
      LEFT JOIN protocolPurpose_file_association ON protocolPurpose_file_association.file_id = file.id 
      LEFT JOIN protocolPurpose ON protocolPurpose.id = protocolPurpose_file_association.protocolPurpose_id 
      LEFT JOIN protocol ON protocol.id = protocolPurpose.protocol_id 

      WHERE protocol.name = 'lp1' 
      AND 
      protocolPurpose.purpose='<purpose>'
      AND 
      protocolPurpose.sgroup='<group>'

    """
    from sqlalchemy import text
    xm2vts = bob.db.xm2vts.Database()
    cuhk   = bob.db.cuhk_cufs.Database()

    #Getting the clients from ARFACE

    sql = "SELECT client.* FROM client "\
          "LEFT JOIN file ON file.client_id = client.id "\
          "LEFT JOIN protocolPurpose_file_association ON protocolPurpose_file_association.file_id = file.id "\
          "LEFT JOIN protocolPurpose ON protocolPurpose.id = protocolPurpose_file_association.protocolPurpose_id "\
          "LEFT JOIN protocol ON protocol.id = protocolPurpose.protocol_id " \
          "WHERE protocol.name = 'lp1'"\
          "AND protocolPurpose.sgroup='"+ group +"'"
 
    clients = xm2vts.query(bob.db.xm2vts.Client).from_statement(text(sql)).all()

    #Getting the correspondent files from bob.db.cuhk_cufs
    files = []    
    for c in clients:
      cuhk_files = cuhk.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_id==c.id)
      #print "{0} = {1}".format(c.id, cuhk_files.count())
      for f in cuhk_files:
        files.append(f)

    return files




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


  def get_clients_from_group(self, group=""):
    """
    This is a hand made protocol since there is no protocol for the CUHK-CUFS database.

    For that I shuffled the indexes of the 188 clients and will take:
      - 40% for training --> 75
      - 30% for developement --> 56
      - 30% for testing --> 57
    """   
   
    indexes = [152, 70, 150, 120, 181, 64, 16, 66, 154, 1, 84, 35, 179, 105, 49, 159, 128, 14, 103, 157, 18, 148, 88, 134, 147, 72, 62, 110, 20, 27, 30, 187, 50, 117, 83, 71, 81, 61, 185, 85, 2, 145, 138, 45, 129, 151, 96, 132, 146, 87, 156, 173, 73, 38, 125, 69, 82, 34, 116, 102, 136, 91, 7, 143, 109, 112, 115, 63, 33, 165, 104, 170, 76, 36, 114, 5, 142, 90, 60, 40, 93, 67, 180, 77, 106, 130, 135, 124, 118, 6, 39, 97, 121, 4, 74, 86, 57, 24, 65, 167, 184, 163, 47, 169, 94, 8, 58, 126, 166, 15, 172, 11, 89, 162, 42, 98, 22, 133, 78, 175, 0, 160, 92, 37, 161, 17, 26, 122, 137, 164, 99, 149, 32, 95, 144, 46, 155, 168, 48, 182, 23, 80, 10, 140, 9, 55, 29, 113, 12, 54, 158, 52, 41, 119, 183, 25, 131, 107, 176, 31, 111, 108, 123, 79, 153, 178, 139, 51, 13, 177, 141, 171, 101, 3, 43, 68, 56, 21, 75, 28, 53, 44, 19, 174, 100, 127, 186, 59]
 
    #Fetching the clients
    cuhk   = bob.db.cuhk_cufs.Database()
    import sqlalchemy
    all_clients = numpy.array(cuhk.query(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.original_database=="cuhk").order_by(bob.db.cuhk_cufs.Client.id).options(sqlalchemy.orm.subqueryload(bob.db.cuhk_cufs.Client.files)).all())

    data_training = 75
    data_dev      = 56
    data_eval     = 57

    clients = []
    if(group=="world"):
      offset = 0
      clients = all_clients[indexes[offset:offset+data_training]]
    elif(group=="dev"):
      offset = data_training
      clients = all_clients[indexes[offset:offset+data_dev]]
    else: 
      offset  = data_training + data_dev
      clients = all_clients[indexes[offset:offset+data_eval]]
 
    #Fetching the correspondent files from bob.db.cuhk_cufs
    #files = []    
    #for c in clients:
      #cuhk_files = cuhk.query(bob.db.cuhk_cufs.File).join(bob.db.cuhk_cufs.Client).filter(bob.db.cuhk_cufs.Client.id==c.id)
      #for f in cuhk_files:
        #files.append(f)

    return list(clients)
 


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

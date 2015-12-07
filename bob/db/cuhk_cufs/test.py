#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu Oct 09 11:27:27 CEST 2014
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

"""A few checks on the protocols of a subset of the CUHK database
"""

import bob.db.cuhk_cufs
#possible_protocols  = ["cuhk"]

""" Defining protocols. Yes, they are static """
PROTOCOLS = ('cuhk_p2s', 'arface_p2s', 'xm2vts_p2s', 'all-mixed_p2s',
             'cuhk_s2p', 'arface_s2p', 'xm2vts_s2p', 'all-mixed_s2p',
             'search_split1_p2s','search_split2_p2s','search_split3_p2s','search_split4_p2s','search_split5_p2s',
             'search_split1_s2p','search_split2_s2p','search_split3_s2p','search_split4_s2p','search_split5_s2p')

GROUPS    = ('world', 'dev', 'eval')

PURPOSES   = ('train', 'enroll', 'probe')



def test01_protocols_purposes_groups():
  
  #testing protocols
  possible_protocols = bob.db.cuhk_cufs.Database().protocols()
  for p in possible_protocols:
    assert p  in PROTOCOLS

  #testing purposes
  possible_purposes = bob.db.cuhk_cufs.Database().purposes()
  for p in possible_purposes:
    assert p  in PURPOSES

  #testing GROUPS
  possible_groups = bob.db.cuhk_cufs.Database().groups()
  for p in possible_groups:
    assert p  in GROUPS



def test02_search_files_protocols():

  total_data = 808+404
  world      = 808
  dev        = 404
  dev_enroll = 202
  dev_probe  = 202
  
  
  protocols = bob.db.cuhk_cufs.Database().protocols()
  for p in protocols:
  
    if "search" in p:  
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p)) == total_data
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="world")) == world

      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev")) == dev
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="enroll")) == dev_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="probe"))  == dev_probe
          
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval")) == 0

  p = "search_split1_p2s"
  assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="enroll", model_ids=[5])) == 1
  assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="probe", model_ids=[5]))  == dev_probe      



def test03_verification_arface_protocols():

  total_data = 88+80+78
  world      = 88
  
  dev        = 80
  dev_enroll = 40
  dev_probe  = 40

  eval        = 78
  eval_enroll = 39
  eval_probe  = 39

  protocols = bob.db.cuhk_cufs.Database().protocols()
  for p in protocols:
    if "arface" in p:  
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p)) == total_data
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="world")) == world

      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev")) == dev
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="enroll")) == dev_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="probe"))  == dev_probe
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval")) == eval
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="enroll")) == eval_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="probe"))  == eval_probe



def test04_verification_xm2vts_protocols():

  total_data = 118*2+88*2+89*2
  world      = 118*2
  
  dev        = 88*2
  dev_enroll = 88
  dev_probe  = 88

  eval        = 89*2
  eval_enroll = 89
  eval_probe  = 89

  protocols = bob.db.cuhk_cufs.Database().protocols()
  for p in protocols:
    if "xm2vts" in p:  
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p)) == total_data
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="world")) == world

      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev")) == dev
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="enroll")) == dev_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="probe"))  == dev_probe
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval")) == eval
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="enroll")) == eval_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="probe"))  == eval_probe



def test05_verification_cuhk_protocols():

  total_data = 75*2 + 56*2 + 57*2
  world      = 75*2
  
  dev        = 56*2
  dev_enroll = 56
  dev_probe  = 56

  eval        = 57*2
  eval_enroll = 57
  eval_probe  = 57

  protocols = bob.db.cuhk_cufs.Database().protocols()  
  for p in protocols:
    if "cuhk" in p:  
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p)) == total_data
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="world")) == world

      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev")) == dev
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="enroll")) == dev_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="dev", purposes="probe"))  == dev_probe
    
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval")) == eval
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="enroll")) == eval_enroll
      assert len(bob.db.cuhk_cufs.Database().objects(protocol=p, groups="eval", purposes="probe"))  == eval_probe



def test06_search_clients_protocols():

  world      = 404
  dev        = 202
      
  protocols = bob.db.cuhk_cufs.Database().protocols()
  for p in protocols:
  
    if "search" in p:  
      assert len(bob.db.cuhk_cufs.Database().model_ids(protocol=p, groups="world")) == world
      assert len(bob.db.cuhk_cufs.Database().model_ids(protocol=p, groups="dev")) == dev


def test07_search_tobjects():

  world      = 404
  protocols = bob.db.cuhk_cufs.Database().protocols()  
  for p in protocols:
    if "search" in p:
      assert len(bob.db.cuhk_cufs.Database().tobjects(protocol=p)) == world
      assert len(bob.db.cuhk_cufs.Database().tclients(protocol=p)) == world
      assert len(bob.db.cuhk_cufs.Database().tmodel_ids(protocol=p)) == world



def test08_strings():
  
  db = bob.db.cuhk_cufs.Database()

  for p in PROTOCOLS:
    for g in GROUPS:
      for u in PURPOSES:
        files = db.objects(purposes=u, groups=g, protocol=p)

        for f in files:
          #Checking if the strings are correct 
          assert f.purpose  == u
          assert f.protocol == p
          assert f.group    == g
       

def test09_annotations():

  db = bob.db.cuhk_cufs.Database()

  for p in PROTOCOLS:
    for f in db.objects(protocol=p):    

      assert len(f.annotations(annotation_type=""))==35 #ALL ANNOTATIONS

      assert f.annotations()["reye"][0] > 0
      assert f.annotations()["reye"][1] > 0

      assert f.annotations()["leye"][0] > 0
      assert f.annotations()["leye"][1] > 0



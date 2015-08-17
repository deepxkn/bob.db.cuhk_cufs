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
PROTOCOLS = ('cuhk_p2s', 'arface_p2s', 'xm2vts_p2s', 'all-mixed_p2s', 'cuhk-arface-xm2vts_p2s', 'cuhk-xm2vts-arface_p2s',
  'arface-cuhk-xm2vts_p2s', 'arface-xm2vts-cuhk_p2s', 'xm2vts-cuhk-arface_p2s', 'xm2vts-arface-cuhk_p2s',
  'cuhk_s2p', 'arface_s2p', 'xm2vts_s2p', 'all-mixed_s2p', 'cuhk-arface-xm2vts_s2p', 'cuhk-xm2vts-arface_s2p',
  'arface-cuhk-xm2vts_s2p', 'arface-xm2vts-cuhk_s2p', 'xm2vts-cuhk-arface_s2p', 'xm2vts-arface-cuhk_s2p')

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


def test02_all_files_protocols():

  cuhk = 376
  arface = 246 
  xm2vts = 590
  all_mixed = 1212
  cuhk_arface_xm2vts = 408
  cuhk_xm2vts_arface = 404
  arface_cuhk_xm2vts = 378
  arface_xm2vts_cuhk = 378
  xm2vts_cuhk_arface = 426
  xm2vts_arface_cuhk = 430
   
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk_p2s")) == cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk_s2p")) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface_p2s")) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface_s2p")) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="xm2vts_p2s")) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="xm2vts_s2p")) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="all-mixed_p2s")) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="all-mixed_s2p")) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk-arface-xm2vts_p2s")) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk-arface-xm2vts_s2p")) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk-xm2vts-arface_p2s")) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="cuhk-xm2vts-arface_s2p")) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface-xm2vts-cuhk_p2s")) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface-xm2vts-cuhk_s2p")) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface-cuhk-xm2vts_p2s")) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="arface-cuhk-xm2vts_s2p")) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(protocol="xm2vts-cuhk-arface_p2s")) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(protocol="xm2vts-cuhk-arface_s2p")) == xm2vts_cuhk_arface


def test03_world_files_protocols():

  cuhk = 150
  arface = 88 
  xm2vts = 236
  all_mixed = 474
  cuhk_arface_xm2vts = cuhk
  cuhk_xm2vts_arface = cuhk
  arface_cuhk_xm2vts = arface
  arface_xm2vts_cuhk = arface
  xm2vts_cuhk_arface = xm2vts
  xm2vts_arface_cuhk = xm2vts
   
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk_p2s")) == cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk_s2p")) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface_p2s")) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface_s2p")) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="xm2vts_p2s")) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="xm2vts_s2p")) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="all-mixed_p2s")) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="all-mixed_s2p")) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk-arface-xm2vts_p2s")) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk-arface-xm2vts_s2p")) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk-xm2vts-arface_p2s")) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="cuhk-xm2vts-arface_s2p")) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface-xm2vts-cuhk_p2s")) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface-xm2vts-cuhk_s2p")) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface-cuhk-xm2vts_p2s")) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="arface-cuhk-xm2vts_s2p")) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="xm2vts-cuhk-arface_p2s")) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='world', protocol="xm2vts-cuhk-arface_s2p")) == xm2vts_cuhk_arface



def test04_dev_files_protocols():

  cuhk = 112
  arface = 80 
  xm2vts = 176
  all_mixed = 368
  cuhk_arface_xm2vts = arface
  cuhk_xm2vts_arface = xm2vts
  arface_cuhk_xm2vts = cuhk
  arface_xm2vts_cuhk = xm2vts
  xm2vts_cuhk_arface = cuhk
  xm2vts_arface_cuhk = arface
   
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk_p2s")) == cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk_s2p")) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface_p2s")) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface_s2p")) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="xm2vts_p2s")) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="xm2vts_s2p")) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="all-mixed_p2s")) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="all-mixed_s2p")) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk-arface-xm2vts_p2s")) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk-arface-xm2vts_s2p")) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk-xm2vts-arface_p2s")) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="cuhk-xm2vts-arface_s2p")) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface-xm2vts-cuhk_p2s")) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface-xm2vts-cuhk_s2p")) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface-cuhk-xm2vts_p2s")) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="arface-cuhk-xm2vts_s2p")) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="xm2vts-cuhk-arface_p2s")) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='dev', protocol="xm2vts-cuhk-arface_s2p")) == xm2vts_cuhk_arface



def test05_eval_files_protocols():

  cuhk = 114
  arface = 78 
  xm2vts = 178
  all_mixed = 370
  cuhk_arface_xm2vts = xm2vts
  cuhk_xm2vts_arface = arface
  arface_cuhk_xm2vts = xm2vts
  arface_xm2vts_cuhk = cuhk
  xm2vts_cuhk_arface = arface
  xm2vts_arface_cuhk = cuhk
   
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk_p2s")) == cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk_s2p")) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface_p2s")) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface_s2p")) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="xm2vts_p2s")) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="xm2vts_s2p")) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="all-mixed_p2s")) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="all-mixed_s2p")) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk-arface-xm2vts_p2s")) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk-arface-xm2vts_s2p")) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk-xm2vts-arface_p2s")) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="cuhk-xm2vts-arface_s2p")) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface-xm2vts-cuhk_p2s")) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface-xm2vts-cuhk_s2p")) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface-cuhk-xm2vts_p2s")) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="arface-cuhk-xm2vts_s2p")) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="xm2vts-cuhk-arface_p2s")) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(groups='eval', protocol="xm2vts-cuhk-arface_s2p")) == xm2vts_cuhk_arface


def test06_dev_enrol_files_protocols():

  cuhk = 56
  arface = 40 
  xm2vts = 88
  all_mixed = 184
  cuhk_arface_xm2vts = arface
  cuhk_xm2vts_arface = xm2vts
  arface_cuhk_xm2vts = cuhk
  arface_xm2vts_cuhk = xm2vts
  xm2vts_cuhk_arface = cuhk
  xm2vts_arface_cuhk = arface
  
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk_p2s"))== cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk_s2p")) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface_p2s")) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface_s2p")) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts_p2s")) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts_s2p")) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="all-mixed_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="all-mixed_p2s")) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="all-mixed_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="all-mixed_s2p")) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk-arface-xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-arface-xm2vts_p2s")) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk-arface-xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-arface-xm2vts_s2p")) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk-xm2vts-arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-xm2vts-arface_p2s")) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="cuhk-xm2vts-arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-xm2vts-arface_s2p")) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface-xm2vts-cuhk_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-xm2vts-cuhk_p2s")) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface-xm2vts-cuhk_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-xm2vts-cuhk_s2p")) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface-cuhk-xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-cuhk-xm2vts_p2s")) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="arface-cuhk-xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-cuhk-xm2vts_s2p")) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="xm2vts-cuhk-arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts-cuhk-arface_p2s")) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='dev', protocol="xm2vts-cuhk-arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts-cuhk-arface_s2p")) == xm2vts_cuhk_arface



def test07_eval_enrol_files_protocols():

  cuhk = 57
  arface = 39 
  xm2vts = 89
  all_mixed = 185
  cuhk_arface_xm2vts = xm2vts
  cuhk_xm2vts_arface = arface
  arface_cuhk_xm2vts = xm2vts
  arface_xm2vts_cuhk = cuhk
  xm2vts_cuhk_arface = arface
  xm2vts_arface_cuhk = cuhk
  
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk_p2s", groups='eval'))== cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk_s2p", groups='eval')) == cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface_p2s", groups='eval')) == arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface_s2p", groups='eval')) == arface

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts_p2s", groups='eval')) == xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts_s2p", groups='eval')) == xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="all-mixed_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="all-mixed_p2s", groups='eval')) == all_mixed
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="all-mixed_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="all-mixed_s2p", groups='eval')) == all_mixed

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk-arface-xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-arface-xm2vts_p2s", groups='eval')) == cuhk_arface_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk-arface-xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-arface-xm2vts_s2p", groups='eval')) == cuhk_arface_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk-xm2vts-arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-xm2vts-arface_p2s", groups='eval')) == cuhk_xm2vts_arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="cuhk-xm2vts-arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="cuhk-xm2vts-arface_s2p", groups='eval')) == cuhk_xm2vts_arface

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface-xm2vts-cuhk_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-xm2vts-cuhk_p2s", groups='eval')) == arface_xm2vts_cuhk
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface-xm2vts-cuhk_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-xm2vts-cuhk_s2p", groups='eval')) == arface_xm2vts_cuhk

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface-cuhk-xm2vts_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-cuhk-xm2vts_p2s", groups='eval')) == arface_cuhk_xm2vts
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="arface-cuhk-xm2vts_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="arface-cuhk-xm2vts_s2p", groups='eval')) == arface_cuhk_xm2vts

  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="xm2vts-cuhk-arface_p2s")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts-cuhk-arface_p2s", groups='eval')) == xm2vts_cuhk_arface
  assert len(bob.db.cuhk_cufs.Database().objects(purposes='enroll', groups='eval', protocol="xm2vts-cuhk-arface_s2p")) == len(bob.db.cuhk_cufs.Database().enroll_files(protocol="xm2vts-cuhk-arface_s2p", groups='eval')) == xm2vts_cuhk_arface


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



 



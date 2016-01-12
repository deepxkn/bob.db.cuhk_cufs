#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Thu 12 Nov 2015 16:35:08 CET 
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

"""
This script will print a list of miss classification per identity
"""

import bob.io.base
import bob.io.image
import bob.measure

import argparse
import numpy, math
import os
import bob.db.cuhk_cufs

# enable LaTeX interpreter

import bob.core
logger = bob.core.log.setup("bob.bio.base")



def command_line_arguments(command_line_parameters):
  """Parse the program options"""

  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('score_file',  help = "The file with the scores of the development set.")
  
  parser.add_argument('preprocess_dir', help = "The directory with the pre-processed files.")  
  
  parser.add_argument('-o', '--output-dir', default="./temp", help = "The output directory.")

  parser.add_argument('-e', '--extension', default=".hdf5", help = "The extension of the files.")

  parser.add_argument('-p', '--protocol', default="search_split1_p2s", help = "Protocol to be executed")

  # add verbose option
  bob.core.log.add_command_line_option(parser)

  # parse arguments
  args = parser.parse_args(command_line_parameters)

  # set verbosity level
  bob.core.log.set_verbosity_level(logger, args.verbose)

  return args



def normalize4save(img):
  return (255 * ((img - numpy.min(img)) / (numpy.max(img)-numpy.min(img)))).astype("uint8")



def get_scores_from_client(score_file, client_id):
  """
  Organize the scores in genuine and the impostor 
  """

  output = {}
  output['genuine'] = []
  output['impostor']  =  []

  for client, probe, file_name, score in bob.measure.load.four_column(score_file):
    
    if(int(client)==int(client_id)):

      if(int(client)==int(probe)):
        output['genuine'].append([file_name,score])
      else:
        output['impostor'].append([file_name,score])
        
  return output
  


def generate_html_output(client_id, scores, img_dir, db, args):
  """
  For each client, will compute the RR and return the pair of comparisons
  """  

  enroll_files = db.objects(protocol=args.protocol, groups="dev", purposes="enroll", model_ids=[client_id])

  enroll_html = ""
  for e in enroll_files:
    img      = normalize4save(bob.io.base.load(os.path.join(args.preprocess_dir, e.path)+args.extension))
    img_file = os.path.join(img_dir,e.path)+".jpg"
    bob.io.base.create_directories_safe(os.path.dirname(img_file))
    bob.io.base.save(img, img_file)
    enroll_html += "<img src='{0}'>".format(img_file.replace(args.output_dir,"./"))

  genuine_html = "<tr><th colspan='3'><b>Client {0}</b></th></tr>\n".format(client_id)
  min_genuine_score = numpy.inf
  for genuine in scores['genuine']:
    img_file = os.path.join(args.preprocess_dir, genuine[0])+args.extension
    img = normalize4save(bob.io.base.load(img_file))
    img_file = os.path.join(img_dir,genuine[0])+".jpg"
    
    bob.io.base.create_directories_safe(os.path.dirname(img_file))      
    bob.io.base.save(img, img_file)
    genuine_html += "<tr><td>" + enroll_html + "</td> <td>" + "<img src='{0}'>".format(img_file.replace(args.output_dir,"./")) + "</td> <td style=\"color:blue;\"> <b>" + str(genuine[1]) + "</b></td> </tr>\n"
    min_genuine_score = min(min_genuine_score, genuine[1])
  
  
  impostor_html = ""
  for impostor in scores['impostor']:  
    #Do only when the score of the impostor is bigger than the genuine score
    if(impostor[1] > min_genuine_score):
      img_file = os.path.join(args.preprocess_dir, impostor[0])+args.extension
      img = normalize4save(bob.io.base.load(img_file))
      img_file = os.path.join(img_dir,impostor[0])+".jpg"
      bob.io.base.create_directories_safe(os.path.dirname(img_file))
      bob.io.base.save(img, img_file)
      impostor_html += "<tr><td>" + enroll_html + "</td> <td>" + "<img src='{0}'>".format(img_file.replace(args.output_dir,"./")) + "</td> <td style=\"color:red;\"><b>" + str(impostor[1]) + "</b></td> </tr>\n"
      
    #Print the columns only if has false acceptance
  if(impostor_html!=""):
    return genuine_html + impostor_html
  else:
    return ""

  

def main(command_line_parameters=None):
  """Reads score files, computes error measures and plots curves."""

  args = command_line_arguments(command_line_parameters)

  db = bob.db.cuhk_cufs.Database(original_directory = args.preprocess_dir, original_extension=args.extension)
  clients = db.clients(protocol=args.protocol, groups="dev")

  img_dir = os.path.join(args.output_dir,"img")
  bob.io.base.create_directories_safe(args.output_dir)
  bob.io.base.create_directories_safe(img_dir)


  html = "<html><body>\n"
  html += " <style type=\"text/css\">\n"
  html += "table, th, td {border: 1px solid black;}\n" 
  html += "table,p {font-size:16px;font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; border-spacing: 0; width: 100%; }"
  html += "td,th,p { border: 1px solid #ddd; text-align: left; padding: 8px;}"
  html += "th { padding-top: 11px; padding-bottom: 11px; background-color: #4CAF50; color: white; text-align: center}"
  html +="</style>\n"

  html += " <p>Score file {0} </br> Protocol: {1} </br> Recognition rate: <b>{2}</b> </p>".format(args.score_file, args.protocol ,bob.measure.recognition_rate(bob.measure.load.cmc_four_column(args.score_file)))
  html += " <table border='0'>\n"
  i = 1
  for c in clients:
    print("Processing client {0} of {1}".format(i, len(clients)))
    i = i + 1
    scores = get_scores_from_client(args.score_file, c.id)
    html += generate_html_output(c.id, scores, img_dir, db, args)
      
  html += "</table>\n"
  html += "</body></html>\n"

  open(os.path.join(args.output_dir,"index.html"),'w').write(html)
  
  
    
    



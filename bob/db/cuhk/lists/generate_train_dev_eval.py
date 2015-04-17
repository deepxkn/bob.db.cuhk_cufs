"""
This script is not part of the package, it is just for organize it.

This script generates the train set, dev set and evaluation set for a given input file.

Since in all protocols of this database we have only one pair per identity, we will define the number of identies as #lines/2

photo first, sketch after

"""

import numpy

input_file  = "all-cuhk.lst"
files_train = 57
files_dev   = 56
files_eval  = 75
files = open(input_file).readlines()

N = len(files)/2
assert N == files_train + files_dev + files_eval

indexes = numpy.array(range(N))
numpy.random.shuffle(indexes)


def get_lines_from_file(files, line_number):

  text = ""
  text += files[line_number]
  text += files[line_number+1]
  
  return text
  
#train set
i = 0
train_text = ""
for j in range(files_train):
  train_text += get_lines_from_file(files, indexes[i]*2)
  i+=1
open("train_world.lst","w").write(train_text)


#dev set
dev_models_text = ""
dev_probes_text = ""
for j in range(files_dev):
  text = get_lines_from_file(files, indexes[i]*2)  
  dev_models_text += text.split("\n")[0] + " " + text.split("\n")[0].split(" ")[1] + "\n"
  dev_probes_text += text.split("\n")[1] + "\n"  
  
  i+=1
open("for_models.lst","w").write(dev_models_text)
open("for_probes.lst","w").write(dev_probes_text)


#eval set
eval_models_text = ""
eval_probes_text = ""
for j in range(files_eval):
  text = get_lines_from_file(files, indexes[i]*2)  
  eval_models_text += text.split("\n")[0] + " " + text.split("\n")[0].split(" ")[1] + "\n"
  eval_probes_text += text.split("\n")[1] + "\n"  
  
  i+=1
open("eval_for_models.lst","w").write(eval_models_text)
open("eval_for_probes.lst","w").write(eval_probes_text)



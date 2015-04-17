"""
This script is not part of the package, it is just for organize it.
"""

import os

HTML_OUTPUT = False


def search_photo2sketch(photo_file_name, sketches):

  prefix = photo_file_name.split("-")[0]
  id     = photo_file_name.split("-")[1]
  
  for s in sketches:

    prefix_s = s.split("-")[0]
    id_s     = s.split("-")[1]

    #if id=="040" and id_s=="040" and id==id_s:
      #import ipdb; ipdb.set_trace();
#    print prefix  + "  --  " + prefix_s
    
    if prefix=="f" and prefix_s=="F2" and id == id_s:
      return s
    elif prefix=="f" and prefix_s=="f" and id == id_s:
      return s
    elif prefix=="f1" and prefix_s=="f1" and id == id_s:
      return s
    elif prefix=="m" and (prefix_s=="m" or prefix_s=="M2") and id == id_s:
      return s
    elif prefix=="m1" and prefix_s=="m1"and id == id_s:
      return s
  return ""
        

input_dir    = "/idiap/resource/database/CUHK-CUFS/CUHK-student-dataset/"
sketches_dir = os.path.join(input_dir,"sketches")
photos_dir   = os.path.join(input_dir,"photos")

sketches = open("sketches").readlines()
photos   = open("photos").readlines()


if not HTML_OUTPUT:

  text = ""
 
  for p in photos:
    sketch_file = search_photo2sketch(p, sketches)
    
    prefix = p.split("-")[0]
    id     = p.split("-")[1]
    
    text += os.path.join("photos",p.rstrip("*\n"))           + " " + prefix + id + "\n"
    text += os.path.join("sketches",sketch_file.rstrip("*\n")) + " " + prefix + id + "\n"    
    
  open("all.lst",'w').write(text)

  
else:

  html = "<html><body>"
  html += "<table>"

  for p in photos:

    html += "<tr>"

    html += "<td><img src='file://"+ os.path.join(photos_dir, p.rstrip("*\n")) +"'></td>"
    sketch_file = search_photo2sketch(p, sketches)
    html += "<td><img src='"+ os.path.join(sketches_dir, sketch_file.rstrip("*\n")) +"'></td>"
  
    html += "</tr>\n"

  html += "</table>"
  html += "</body></html>"

  open("output.html",'w').write(html)

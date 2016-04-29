.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. Thu Apr 16 16:39:01 CEST 2015


.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.cuhk_cufs/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.cuhk_cufs/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.db.cuhk_cufs.svg?branch=v1.0.1
   :target: https://travis-ci.org/bioidiap/bob.db.cuhk_cufs
.. image:: https://coveralls.io/repos/bioidiap/bob.db.cuhk_cufs/badge.svg?branch=v1.0.1
   :target: https://coveralls.io/r/bioidiap/bob.db.cuhk_cufs
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.db.cuhk_cufs/tree/master
.. image:: http://img.shields.io/pypi/v/bob.db.cuhk_cufs.png
   :target: https://pypi.python.org/pypi/bob.db.cuhk_cufs
.. image:: https://img.shields.io/badge/original-data--files-a000a0.png
   :target: http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html


=======================================================
 CUHK Face Sketch Database (CUFS)
=======================================================

This package contains the access API and descriptions for the `CUHK Face Sketch Database (CUFS) <http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html>`. 
The actual raw data for the database should be downloaded from the original URL. 
This package only contains the Bob accessor methods to use the DB directly from python, with the original protocol of the database.

CUHK Face Sketch database (CUFS) is for research on face sketch synthesis and face sketch recognition.
It includes 188 faces from the Chinese University of Hong Kong (CUHK) student database, 123 faces from the AR database, and 295 faces from the XM2VTS database.
There are 606 faces in total.
For each face, there is a sketch drawn by an artist based on a photo taken in a frontal pose, under normal lighting condition, and with a neutral expression.


You would normally not install this package unless you are maintaining it. 
What you would do instead is to tie it in at the package you need to **use** it.
There are a few ways to achieve this:

1. You can add this package as a requirement at the ``setup.py`` for your own
   `satellite package
   <https://github.com/idiap/bob/wiki/Virtual-Work-Environments-with-Buildout>`_
   or to your Buildout ``.cfg`` file, if you prefer it that way. With this
   method, this package gets automatically downloaded and installed on your
   working environment, or

2. You can manually download and install this package using commands like
   ``easy_install`` or ``pip``.

The package is available in two different distribution formats:

1. You can download it from `PyPI <http://pypi.python.org/pypi>`_, or

2. You can download it in its source form from `its git repository
   <https://github.com/bioidiap/bob.db.cuhk_cufs>`_.

You can mix and match points 1/2 and a/b above based on your requirements. Here
are some examples:

Modify your setup.py and download from PyPI
===========================================

That is the easiest. Edit your ``setup.py`` in your satellite package and add
the following entry in the ``install_requires`` section (note: ``...`` means
`whatever extra stuff you may have in-between`, don't put that on your
script)::

    install_requires=[
      ...
      "bob.db.cuhk_cufs",
    ],

Proceed normally with your ``boostrap/buildout`` steps and you should be all
set. That means you can now import the ``bob.db.cuhk_cufs`` namespace into your scripts.

Modify your buildout.cfg and download from git
==============================================

You will need to add a dependence to `mr.developer
<http://pypi.python.org/pypi/mr.developer/>`_ to be able to install from our
git repositories. Your ``buildout.cfg`` file should contain the following
lines::

  [buildout]
  ...
  extensions = mr.developer
  auto-checkout = *
  eggs = bob.db.cuhk_cufs

  [sources]
  bob.db.cuhk_cufs = git https://github.com/bioidiap/bob.db.cuhk_cufs.git
  ...

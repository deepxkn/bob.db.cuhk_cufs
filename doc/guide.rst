.. vim: set fileencoding=utf-8 :
.. @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
.. @date:   Thu 03 Dec 2015 17:51:44 CET 

==============
 User's Guide
==============

This package contains the access API and descriptions for the CUHK Face Sketch Database (`CUFS`_) database.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded from the original URL.

The Database Interface
----------------------

The :py:class:`bob.db.cuhk_cufs.Database` complies with the standard biometric verification database as described in :ref:`commons`, implementing both interfaces :py:class:`bob.db.verification.utils.SQLiteDatabase` and :py:class:`bob.db.verification.utils.ZTDatabase`.


CUHK CUFS Protocols
--------------------


For this database we developed two major blocks of protocols. One for face **identification** (search) and one for face **verification** (comparison).


Search protocols
================

Defines a set of protocols for VIS->Skectch and Sketch->VIS face identification (search) in a **close-set**.
These protocols were organized in the same way as in::

   @article{klare2013heterogeneous,
     title={Heterogeneous face recognition using kernel prototype similarities},
     author={Klare, Brendan F and Jain, Anil K},
     journal={Pattern Analysis and Machine Intelligence, IEEE Transactions on},
     volume={35},
     number={6},
     pages={1410--1422},
     year={2013},
     publisher={IEEE}
  }

For each task (VIS->Sketch or Sketch->VIS) the 606 subjects are split in **5 sets** where:
 - 404 subjects are used for training
 - 202 subjects are used for evaluation

To fetch the object files using, lets say the first split for the VIS->sketch protocol, use the following piece of code:

.. code-block:: python

   >>> import bob.db.cufs
   >>> db = bob.db.cufs.Database()
   >>>
   >>> #fetching the files for training   
   >>> training = db.objects(protocol="search_split1_p2s", groups="world")
   >>>
   >>> #fetching the files for testing
   >>> galery =  db.objects(protocol="search_split1_p2s", groups="dev", purposes="enroll")
   >>> probes =  db.objects(protocol="search_split1_p2s", groups="dev", purposes="probe")
   >>>


To list the available protocols type:

.. code-block:: python

   >>> import bob.db.cufs
   >>> db = bob.db.cufs.Database()
   >>> print(db.protocols())


Comparison protocols
====================

Defines a set of protocols for VIS->Skectch and Sketch->VIS face verification (comparison).
These set of protocols were designed by IDIAP Research Institute team.


There are four protocols for each task (VIS->Sketch or Sketch->VIS) and, for each one, the 606 subjects are split in the sets:

- ARFACE set (```arface_p2s``` and ```arface_s2p```)
  In this set of protocols only pair of images of the ARFACE database are considered. The 123 pairs are split in:
  
  * 44 subjects are used for training
  * 40 subjects are used for development
  * 39 subjects are used for evaluation
 

- XM2VTS set (```xm2vts_p2s``` and ```xm2vts_s2p```)
  In this set of protocols only pair of images of the XM2VTS database are considered. The 295 pairs are split in:
  
  * 118 subjects are used for training
  * 88 subjects are used for development
  * 89 subjects are used for evaluation


- CUHK set (```cuhk_p2s``` and ```cuhk_s2p```)
  In this set of protocols only pair of images of the XM2VTS database are considered. The 188 pairs are split in:
  
  * 75 subjects are used for training
  * 56 subjects are used for development
  * 57 subjects are used for evaluation

- ALL Mixed set (```cuhk_p2s``` and ```cuhk_s2p```). This is a mix of all databases (ARFACE + XM2VTS + CUHK).
  In this set of protocols only pair of images of the XM2VTS database are considered. The 188 pairs are split in:
  
  * 237 subjects are used for training
  * 184 subjects are used for development
  * 185 subjects are used for evaluation


To fetch the object files using, lets say the VIS->sketch comparison protocol for the ARFACE, use the following piece of code:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufs.Database()
   >>>
   >>> #fetching the files for training   
   >>> training = db.objects(protocol="arface_p2s", groups="world")
   >>>
   >>> #fetching the files for development
   >>> galery_dev =  db.objects(protocol="arface_p2s", groups="dev", purposes="enroll")
   >>> probes_dev =  db.objects(protocol="arface_p2s", groups="dev", purposes="probe")
   >>>
   >>> #fetching the files for evaluation
   >>> galery_eval =  db.objects(protocol="arface_p2s", groups="eval", purposes="enroll")
   >>> probes_eval =  db.objects(protocol="arface_p2s", groups="eval", purposes="probe")
   >>>

Score Normalization
====================

This database API also provides methods to get identities for Z-Norm a T-Norm (score normalization techniques) `[BENGIO]`_.

Z-Norm
------

The Z-Norm or Zero Normalization normalize the scores in such a way that allows the selection of a global decision threshold.
The Z-Norm aligns the imposter score distributions of all probes to zero mean and scaling them to unit variance. [`score`_]

The intuition behind Z-Norm in the VIS->Sketch task is to shift the Sketch distribution close to the VIS score distribution. 

To fetch the Z-Norm object files for the first split of the search protocol (just an example), use the following code:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufs.Database()
   >>> zobjects = db.zobjects(protocol="search_split1_p2s")
   
T-Norm
------

The T-Norm or Test Normalization or cohort noalization normalizes the scores at test time (computes statistics for the normalization at test time).
Usually this normalization is carried out, for each identity, against a specific group of identities, a.k.a cohort, which are considered to be "difficult" to recognize.

To fetch the T-Norm object files for the first split of the search protocol (just an example), use the following code:

.. code-block:: python

   >>> import bob.db.cufsf
   >>> db = bob.db.cufs.Database()
   >>> zobjects = db.tobjects(protocol="search_split1_p2s")




.. _CUFS: http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html
.. _bob: https://www.idiap.ch/software/bob
.. _score: http://home.iitk.ac.in/~snitish/Stuff/Score_normalization_report.pdf
.. _[BENGIO]: Mariéthoz, Johnny, and Samy Bengio. "A unified framework for score normalization techniques applied to text-independent speaker verification." Signal Processing Letters, IEEE 12.7 (2005): 532-535.

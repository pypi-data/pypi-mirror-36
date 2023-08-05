.. _gui-introduction-values:

Specifying field values and identifiers
=======================================

Fields for entering text (e.g. names, source code) are tajken literary. 
Fields for entering variables, parameters, options, and settings accept 
several data types

   * integer and real numbers are treated as Python scalars of type 
     ``int`` and ``float``
   * strings ``True`` and ``False`` are treated as scalar boolean values
   * all other strings not containing whitespace are treated as strings
   * space separated values are treated as lists
   
This has several limitations. For instance, you cannot specify a string 
containing whitespace. You also cannot specify an empty list or a list 
with no members. For such cases you can use the hash notation

.. code-block:: none

   #<Pythonic expression>

One would specify an empty list and a list with one element as

.. code-block:: none

   #[]
   #['element']
   
The expression will be evaluated when the data in the GUI are dumped to 
a file, unless otherwise noted. The variables which were defined in the 
project are available in the evaluation environment. 

The following hashed entries in the GUI result in identical dumped values 

.. code-block:: none

   100
   #100
   #50+50
   
   True
   #True
   #1==1
   
   hello 3 4 5
   #['hello', 3, 4, 5]

Identifiers are strings conforming to some simple rules. 

   * An identifier comprises only numbers, English letters, and underscores. 
   * It never starts with a number. 

They are used for naming things in PyOPUS and the GUI. 

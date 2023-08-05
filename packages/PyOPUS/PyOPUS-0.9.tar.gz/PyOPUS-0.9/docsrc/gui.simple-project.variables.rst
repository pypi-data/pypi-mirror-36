Defining variables
==================

We are going to define two variables holding the names of the MOS transistor 
instances and flags specifying whthere these transistors are of NMOS type. 
To see more on how variable values are specifiede read section 
:ref:`gui-introduction-values`. If variable values are given with the hash 
notation as Pythonic expressions the expressions are evaluated in an 
environment that contains no variables. 

.. figure:: gui-project-variables.png
	:scale: 75%
	
	Defining a variable in the GUI. 
	
The value of variable ``mosList`` can be specified as

.. code-block:: none

   xmn1 xmn2 xmn3 xmn4 xmn5 xmp1 xmp2 xmp3
   
or as 

.. code-block:: none

   #['xmn1', 'xmn2', 'xmn3', 'xmn4', 'xmn5', 'xmp1', 'xmp2', 'xmp3']

With the latter syntax we specify the ``isNmos`` variable which is list of 
flags specifying whether a transistor is of type NMOS.  

.. code-block:: none

   #[1, 1, 1, 1, 1, 0, 0, 0]

Variable names must be unique identifiers.

Writing a custom dispatcher
===========================

This time we build a custom asynchronous job dispatcher. Again the function 
:func:`jobProcessor` is defined in file 
`funclib.py <../../../demo/parallel/cooperative/funclib.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: jobProcessor 

File `05-asyncloop.py <../../../demo/parallel/cooperative/05-asyncloop.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_

.. literalinclude:: ../demo/parallel/cooperative/05-asyncloop.py


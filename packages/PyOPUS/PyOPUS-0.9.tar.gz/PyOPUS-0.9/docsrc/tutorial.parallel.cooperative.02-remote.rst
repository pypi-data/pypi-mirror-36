Remote tasks (task outsourcing)
===============================

Suppose you want to outsource tasks to other processors in the system (either in the 
same physical machine or in a remote machine). First the task must be defined as 
a function that returns the task result. The function must be defined in a module so 
that it can be pickled and sent to a remote processor. 

In this example the :func:`printMsgMPI` function is defined in file 
`funclib.py <../../../demo/parallel/cooperative/funclib.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_
It prints message *msg* *n* times along with the host and task ID assigned by the MPI
subsystem. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: printMsgMPI 

The following Python program spawns two concurrent local tasks and two remote tasks. The 
actual CPU where a remote task will run is assigned by MPI. 

File `02-remote.py <../../../demo/parallel/cooperative/02-remote.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_

.. literalinclude:: ../demo/parallel/cooperative/02-remote.py

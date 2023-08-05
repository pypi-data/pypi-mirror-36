Context switching in cooperative multitasking
=============================================

This example demonstrates the use of the cooperative multitasking OS for defining 
concurrent tasks. 

The :func:`printMsg` function is defined in file 
`funclib.py <../../../demo/parallel/cooperative/funclib.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_. 
It prints message *msg* *n* times. After every printout it allows a 
context switch to another task by calling :func:`cOS.Yield`. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: printMsg 

The following Python program spawns two concurrent tasks that print two messages. 
The first one prints it 10 times and the second oen 20 times. After the tasks are 
spawned the program waits for them to finish by using the :func:`cOS.Join` function. 
	
File `01-context.py <../../../demo/parallel/cooperative/01-context.py>`_ 
in folder `demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_

.. literalinclude:: ../demo/parallel/cooperative/01-context.py

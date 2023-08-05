Dispatching an unknown number of tasks, collecting results with a results collector
===================================================================================

Sometimes the number of tasks to dispatch is not known in advance. The time when to stop generating 
tasks may depend on the task results. This example demonstrates how to generate tasks and stop 
when a certain condition is met. 

A job is evaluated by the :func:`jobProcessor` function defined in file 
`funclib.py <../../../demo/parallel/cooperative/funclib.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_.

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: jobProcessor 
	
This time the generator is more complex so we define it as a function. The stopping 
condition is met when the *stopFlag* global variable is set to ``True``. This generator 
generates jobs that multiply values by 2. The values form a sequence starting at *start* 
with step given by *step*. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: dynJobGenerator

By default :func:`cOS.dispatch` collects the results and puts them in a list in the order 
in which the jobs were generated. This time we use a more complex mechanism for colelcting 
the results - a results collector. A results collector is an unprimed coroutine that 
receives results and organizes them in some data structures. This enables us to set the 
*stopFlag* depending on the received result. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: resultsCollector

The *stopFlag* is set when a result is received that is greater or equal to *stopAtResult*. 
In our example the results are stored in a list passed ba the *resultStorage* argument. 
A results collector can detect when there are no more results to collect by catching the 
*GeneratorExit* exception. 

Of course one must also define the *stopFlag*::

  stopFlag=False

Finally we put it all together. 

File `04-dyndispatch.py <../../../demo/parallel/cooperative/04-dyndispatch.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_

.. literalinclude:: ../demo/parallel/cooperative/04-dyndispatch.py

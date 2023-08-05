Dispatching a set of tasks and collecting the results
=====================================================

Outsourcing a set of tasks and collecting the results is simple. You don't have to 
do any calls to :func:`cOS.Spawn` or :func:`cOS.Yield`. Instead you can use
:func:`cOS.dispatch`. 

A job is evaluated by the :func:`jobProcessor` function defined in 
file `funclib.py <../../../demo/parallel/cooperative/funclib.py>`_ 
in folder `demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_. 

.. literalinclude:: ../demo/parallel/cooperative/funclib.py
	:pyobject: jobProcessor 

Every job is specified in the form  of a tuple where the first entry is the function 
and the second entry is the list of the positional arguments. The jobs are generated 
by a generator that is defined with a simple generator expression. 

Dispatching is asynchronous. This means that if you have less processors than jobs a
processor will receive a new job as soon as the previous one is finished. This is 
repeated until all jobs are processed. 

File `03-dispatch.py <../../../demo/parallel/cooperative/03-dispatch.py>`_ in folder 
`demo/parallel/cooperative/ <../../../demo/parallel/cooperative/>`_

.. literalinclude:: ../demo/parallel/cooperative/03-dispatch.py

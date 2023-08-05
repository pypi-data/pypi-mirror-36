Plotting the circuit's response during optimization
===================================================

This demo shows how to plot the circuit's response during optimization. 
Read chapter :ref:`tut-evaluation-optimize` to learn more about circuit 
optimization. 

The problem definition in the main file 
`runme.py <../../../demo/evaluation/06-iteration-plotter/runme.py>`_ in folder 
`demo/evaluation/06-iteration-plotter/ <../../../demo/evaluation/06-iteration-plotter/>`_
is identical to the one in chapter :ref:`tut-evaluation-optimize`. 
Only the differences are given in this document. 

First we import the the things we need. 

.. literalinclude:: ../demo/evaluation/06-iteration-plotter/runme.py
	:start-after: # Imports
	:end-before: # End imports

In the main program we insert an iteration plotter plugin in the optimizer. 

.. literalinclude:: ../demo/evaluation/06-iteration-plotter/runme.py
	:start-after: # Main program
  

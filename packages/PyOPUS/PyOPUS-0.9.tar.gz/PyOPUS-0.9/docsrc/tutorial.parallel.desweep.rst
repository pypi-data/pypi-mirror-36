Performing many differential evolution runs on a cluster of workstations
========================================================================

Suppose we want to evaluate te performance of differential evolution for all combinations 
of *n* population size and *m* test functions. Every function/population size must be run 
*k* times. This gives us k * l * m differential evolution runs which is quite a bit of work. 
Suppose we want to distribute this work to a bunch of computers. 

First we must define a function that runs differential evolution for a given problem 
with a given population size. When a run is finished the function returns the best function 
value found and the function evaluation history. 

File `funclib.py <../../../demo/parallel/desweep/funclib.py>`_ 
in folder `demo/parallel/desweep/ <../../../demo/parallel/desweep/>`_

.. literalinclude:: ../demo/parallel/desweep/funclib.py

Now let's take a look at the main program in file `funclib.py <../../../demo/parallel/desweep/funclib.py>`_ in folder `demo/parallel/desweep/ <../../../demo/parallel/desweep/>`_. 
First we import some things

.. literalinclude:: ../demo/parallel/desweep/depop.py
	:start-after: # Imports
	:end-before: # End imports
	
Next we define the parameters of the run. 

.. literalinclude:: ../demo/parallel/desweep/depop.py
	:start-after: # Settings
	:end-before: # End settings
	
The job generator produces tuples of the form (function, args, kwargs, misc). The last entry 
of the tuple contains miscellaneous data that helps the results collector to organize the 
collected results. This entry does not affect job evaluation. 

.. literalinclude:: ../demo/parallel/desweep/depop.py
	:pyobject: jobGenerator

The results collector is an unprimed coroutine. It writes the function evaluation history 
to a file named ``fhist_f<index>_p<popSize>_r<runIndex>.pck``. It also stores the lowest 
function value in the *finalF* dictionary. 

.. literalinclude:: ../demo/parallel/desweep/depop.py
	:pyobject: resultsCollector

Finally the main part of the program dispatches the generated jobs and writes some summary 
information to a file named ``fsummary.pck``. 

.. literalinclude:: ../demo/parallel/desweep/depop.py
	:start-after: # Main program

You can run the example on a ,local computer in parallel using the available processors with

.. code-block:: none

  mpirun -n <nproc> python depop.py

See :ref:`tut-mpi` on how to run a program across mutiple machines. 

After the run is finished you end up with a bunch of .pck files. To display the stored 
function evaluation history for a particular run, you can use the program in 
File `an.py <../../../demo/parallel/desweep/an.py>`_ 
in folder `demo/parallel/desweep/ <../../../demo/parallel/desweep/>`_

.. literalinclude:: ../demo/parallel/desweep/an.py

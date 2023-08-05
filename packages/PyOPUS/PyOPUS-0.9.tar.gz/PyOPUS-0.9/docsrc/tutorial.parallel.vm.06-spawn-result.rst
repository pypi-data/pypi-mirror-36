Spawning remote tasks and collecting results
============================================

This example spawns remote tasks and then waits for the results. This demo reuqires at least 5 slots 
in the cluster (one for the spawner and 4 for the spawned tasks). 

File `06-spawn-result.py <../../../demo/parallel/vm/06-spawn-result.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_

.. literalinclude:: ../demo/parallel/vm/06-spawn-result.py

The :func:`pyEvaluator` function is defined in the :mod:`funclib` module (file `funclib.py <../../../demo/parallel/vm/funclib.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_). 
The function evaluates the expression that is passed to it as a string and returns the result. 

.. literalinclude:: ../demo/parallel/vm/funclib.py
  :pyobject: pyEvaluator

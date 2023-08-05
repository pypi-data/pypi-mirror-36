.. _parallel-cooperative:
	
Algorithm parallelization
=========================

This tutorial explains how to use the cooperative multitasking OS for introducing concurrency. 
The same OS can be used to outsource concurrent tasks to other procesors to achieve parallel 
processing. Several methods for dispatching tasks are described. Finally an example is given 
where a large number of optimization runs is distributed among multiple processor that 
run them in parallel. 

.. toctree::
   :maxdepth: 2
   
   tutorial.parallel.cooperative.01-context.rst
   tutorial.parallel.cooperative.02-remote.rst
   tutorial.parallel.cooperative.03-dispatch.rst
   tutorial.parallel.cooperative.04-dyndispatch.rst
   tutorial.parallel.cooperative.05-asyncloop.rst
   tutorial.parallel.desweep.rst

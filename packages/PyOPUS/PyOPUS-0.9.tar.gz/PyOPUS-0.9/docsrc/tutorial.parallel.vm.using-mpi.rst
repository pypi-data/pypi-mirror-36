.. _tut-mpi:

Using MPI with PyOPUS
=====================

This tutorial explains how to use the :mod:`pyopus.parallel.vm` module, more specifically
the MPI interface of PyOPUS (module :mod:`pyopus.parallel.mpi`). 


A parallel program using MPI can be started with the ``mpirun`` utility. All examples 
assume you are using the OpenMPI implementation of the MPI specification, but most 
things hold also for other MPI implementations. 

Starting a parallel application on a single computer with multiple processors is simple. 
Suppose you want to start ``example.py`` with 4 processes. To achieve this, you would type

.. code-block:: none

  mpirun -n 4 python example.py

To distribute a run across multiple physical machines, you must first define a hosts file. 
Suppose the file is named ``hosts.openmpi``

.. code-block:: none

  queen slots=4
  worker01 slots=4
  
This specifies two machines (queen and worker01) with 4 process slots each (both machines 
have 4 processors, each of them capable of running a single thread). To start a run with 
8 processes you would type

.. code-block:: none

  mpirun -n 8 --hostfile hosts.openmpi python example.py

Of course you don't have to use up all available slots. To start a run with 6 processes 
type

.. code-block:: none

  mpirun -n 6 --hostfile hosts.openmpi python example.py
  
In this case two of the 8 available processors (slots) are unused. 

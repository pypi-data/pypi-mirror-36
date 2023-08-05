.. _parallel-vm:

Using the virtual machine abstraction layer
===========================================

This tutorial explains the basics of the virtual machine abstraction layer. Currently only MPI 
is supported, but one could add an abstraction of virtually any parallel processing platform 
(i.e. in the past PyOPUS was using PVM in much the same manner as MPI today). The tutorial 
explains how to retrieve the virtual machine configuration, how to spawn functions of remote 
processors, and how to establish communication between tasks. The tutorial also explains how 
to perform file mirroring so that all tasks run in an identical environment that is established 
on a local storage to maximize performance. Finally an example is given that outsources some 
tasks and collects their results. 

.. toctree::
   :maxdepth: 2
   
   tutorial.parallel.vm.using-mpi.rst
   tutorial.parallel.vm.01-config.rst
   tutorial.parallel.vm.02-spawn.rst
   tutorial.parallel.vm.03-messaging.rst
   tutorial.parallel.vm.04-mirror.rst
   tutorial.parallel.vm.05-storage-cleanup.rst
   tutorial.parallel.vm.06-spawn-result.rst


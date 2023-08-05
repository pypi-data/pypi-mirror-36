Running a task in parallel 
==========================

The active task is started in parallel mode by selecting Task/Start on cluster 
in the main menu. The overview of running tasks is available is the MPI hosts 
tab. 

.. figure:: gui-parallel-running-hosts.png
	:scale: 75%
	
	The MPI hosts tab displaying the status of the cluster. 
	
For every host the list of tasks that are tunning on that host is displayed 
along with the number of host's CPUs used for the task. If a task uses 
multiple CPUs one CPU acts as a manager while the remaining CPUs are workers. 
With 8 CPUs you can expect speedups of up to 7. 

.. figure:: gui-parallel-running-summary.png
	:scale: 75%
	
	Summary of the "nominal" task run on 8 CPUs. 

If we start the "nominal" task on 8 CPUs a typical results database looks 
like the above figure. We can see that the task took 82 seconds compared to 
302 seconds on a single CPU. We can see that the optimizer evaluated a 
somewhat larger number of candidate circuits when it was using 8 CPUs. This 
is due to the fact that asynchronous parallel optimizers (like PSADE) can 
take a different path through the design space when run in parallel due to 
the indeterminate nature of communication delays. Nevertheless we obtained 
the result 3.7 times faster. 

A typical start of a parallel run looks like this in the log (the time and the 
PyOPUS subsystem are displayed for the log messages): 
	
.. code-block:: none

   0.0 LNCH: Logging started by launcher process on host calypso, pid=0x76e5 (30437)
   0.0 LNCH: Folder /mnt/data/Data/pytest/demo/gui/miller/nominal
   0.0 LNCH: Engine process (mpirun python3 runme.py) started on host calypso, pid=0x76e9 (30441)
   0.0 LNCH: lock.response file created at task start.
   0.8 VM  : Process list (total 8):
   0.8 VM  :   Host calypso with 8 process(es)
   0.8 VM  :     slot 0: pid=0x76ee (30446)
   0.8 VM  :     slot 1: pid=0x76ef (30447)
   0.8 VM  :     slot 2: pid=0x76f0 (30448)
   0.8 VM  :     slot 3: pid=0x76f1 (30449)
   0.8 VM  :     slot 4: pid=0x76f2 (30450)
   0.8 VM  :     slot 5: pid=0x76f3 (30451)
   0.8 VM  :     slot 6: pid=0x76f4 (30452)
   0.8 VM  :     slot 7: pid=0x76f5 (30453)
   ...

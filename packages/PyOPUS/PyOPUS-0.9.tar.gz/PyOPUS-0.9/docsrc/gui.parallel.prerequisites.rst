Prerequisites for successfull parallelization
=============================================

First of all, the mpi4py library must be installed. This library is a wrapper 
around some MPI library. We will assume throughout this section that under 
Linux the OpenMPI library is the one that is wrapped. For Windows we will 
assume mpi4py wraps the Microsoft MPI library. Under Linux usually the package 
manager handles the installation of OpenMPI automatically when you install 
mpi4py. Under Windows you must manually install Microsoft MPI. 

If you are going to use CPUs across multiple hosts you will need to set up a 
folder that will be shared across all hosts. One way to achieve this is under 
Linux is to set up a NFS shared folder. It is common that the ``/home`` folder 
is mounted via NFS on all machines in a cluster. In this case all you need to 
do is to keep all of your projects somewhere under ``/home``. If. however the 
shared folder is not mounted on the same mountpoint across all hosts you must 
define an environmental variable ``PARALLEL_MIRRORED_STORAGE`` on every host 
that will be used. The variable is a colon separated list of mountpoints. 
An entry in the variable's value is assumed to represent the same physical 
storage on all hosts where the variable is defined. 

Design tasks can generate a lot of output files. These files are read by 
components of PyOPUS. This can easily saturate the network connection when 
shared folders are used. Therefore PyOPUS can perform most of disk read/write 
operations on the local dis of the machine. By default local files are written 
to the temporary folder (``/tmp`` under Linux). If, however, this folder is not 
local or does not have a sufficient amount of available space you can use a 
different folder by defining the ``PARALLEL_LOCAL_STORAGE`` environmental 
variable on every host where you don't want to use the temporary folder. 

When using Microsoft MPI under Windows you must start a program named smpd on 
every host that is going to run PyOPUS tasks by starting a command prompt and 
typing 

.. code-block:: none

   smpd -d 3
   
The ``-d 3`` option will enable debug output which will help you solve 
problems with your MPI setup. 

The GUI autodetects the number of CPUs on the local machine. If you want to 
also use remote machines in your parallel runs you must specify the hosts 
by choosing View/MPI hosts in the main menu and add entries to the table 
of hosts specifying the hostname and the number of available CPUs for every 
host. 

.. figure:: gui-parallel-cluster.png
	:scale: 75%
	
	Defining available hosts and CPU counts. 
	
In the right part of the status bar the number of free and the number of 
available CPUs are displayed. 

.. figure:: gui-parallel-task-mpi.png
	:scale: 75%
	
	MPI settings of a task. 
	
Every task has an "MPI settings" item. Here you can limit the number of CPUs 
that will be used when the task is run in parallel. If nothing is specified 
the task will use all available CPUs in the cluster. 

The "Mirror files to local storage" option enables the creation of a local 
folder for every processor that is running a task via MPI. The files listed 
under the Files item in the Project tree are copied (mirrored) to the local 
folder so that the task is executed in the same environment as it would be 
if run locally. Make sure you list all relevant files under the Files item 
or your remote tasks will produce errors and fail. 

Enabling the "Persistent storage of mirrored data" option will force PyOPUS 
to create a local folder and mirror the files only once for every task 
execution. If disabled, a new local folder is created for every job that is 
outsourced by PyOPUS. This can be expensive and significantly slow down 
the optimization run. On the other hand, when experiencing problems, turn 
off this option. If the behavior improves you probably hit a bug in PyOPUS 
or have bad luck because PyOPUS reused an old local folder (this can happen 
if the remote task has the same PID as a task that was run in the past). To 
avoid the latter make sure the local storage is cleaned up when a host is 
started. 

"MPI debug level" sets the verbosity level of the MPI module in PyOPUS. This 
option is intended for PyOPUS development. 

"Cooperative multitasking manager debug level" sets the verbosity level of 
the cooperative multitasking OS in PyOPUS. This OS is responsible for 
distributing jobs across CPUs. The option is intended for PyOPUS development. 

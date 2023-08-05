The GUI window
==============

The title bar of the GUI window displays the name of the current project. 
The GUI window is divided in several parts:
	
   * The menu bar with basic commands. 
   * Tabs for accessing the project, design tasks, results, logs, etc. 
   * Main part showing the active tab's content
   * Messages
   * Status bar showing the active design task's status and the number 
     of free/available CPUs across the defined machine cluster. 
	
.. figure:: gui-window.png
	:scale: 80%
	
	The GUI window. 
  
When the GUI is started it first looks for a config file (``pyopusgui.config``) 
in the current directory. Next, the host name is detected and the number of 
available CPUs on the host where the GUI was started. The GUI searches for 
supported simulators and when it finds one it displays its location on the 
host where the GUI was started. 

The MPI launcher is detected and its location is printed. The list of 
directories available to all machines in the cluster (mirrored storage) is 
displayed. It can be set with the PARALLEL_MIRRORED_STORAGE environmental 
variable (see :mod:`pyopus.parallel.base` for details). The local storage 
on the host where the GUI was started is printed (can be set with the 
PARALLEL_MIRRORED_STORAGE environmental variable, see :mod:`pyopus.parallel.base`
for details). 

A typical output in the message window looks like this:

.. code-block:: none

   Failed to load '/mnt/data/Data/pytest/docsrc/pyopusgui.config'. Using defaults.
   Running on host 'calypso' with 8 CPU(s).
   Found local simulator Synopsys HSPICE: /sw/hspice/linux/hspice
   Found local simulator Cadence Spectre: /sw/cadence/MMSIM121/tools/bin/spectre
   Found local simulator Spice Opus: /usr/local/bin/spiceopus.bin
   Found MPI launcher: /usr/bin/mpirun
   Local machine's VM mirrored storage:
   -- 1: /home/arpadb
   -- 2: /mnt/data/Data/pytest
   -- 3: /home/arpadb/pytest-3
   -- 4: /mnt/data/Data/pywork
   Local machine's VM local storage: /tmp
   Using PyOPUS GUI file format version 1.0.
   Started a new blank project.
   Current folder is '/mnt/data/Data/pytest/docsrc'.
   Welcome to PyOPUS GUI.
   
The printed information is for debugging purposes only. It does not impose 
any limitations on the options available in the GUI. It can, however, be 
helpful when you are trying to find the cause for a problem. 

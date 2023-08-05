Data mirroring
==============

When mirroring is enabled a local storage folder is created for every spawned task. The task is then 
started in this folder. The location where this folder is created is determined by the 
``PARALLEL_LOCAL_STORAGE`` environmental variable. If the variable is not set a default location is 
used (i.e. <temporary_folder>/pyopus). 

The temporary folder is populated with files that are specified VM object construction using the 
*mirrorMap* parameter. The copying is performed via shared folders (mounted filesystems). The 
``PARALLEL_MIRRORED_STORAGE`` environmental variable specifies a colon separated list of paths to shared 
folders in the same order on all hosts in the cluster. If the variable is not specified the user's 
home folder is assumed to be shared across all hosts. 

After the spawned process is finished the temporary folder is deleted. If the *persistentStorage* 
parameter is set to ``True`` at VM object construction the storage is not deleted when the task is 
finished and the next time a new task is spawned the same folder is reused. Because temporary folders 
are named after the process ID of the client that executed spawn requests these folders must be 
deleted when the machine is started so that a temporary folder created before the last booting of 
the machine is not reused along with its outdated contents. 

The process ID is an integer and can theoretically wrap around if the system is up for a sufficient 
amount of time. In practice, however, this happens rarely because process IDs are 32-bit integers 
or even longer. 

File `04-mirror.py <../../../demo/parallel/vm/04-mirror.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_

.. literalinclude:: ../demo/parallel/vm/04-mirror.py

The :func:`helloLs` function is defined in the :mod:`funclib` module (file `funclib.py <../../../demo/parallel/vm/funclib.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_). 
This function prints the contents of the currect folder. 

.. literalinclude:: ../demo/parallel/vm/funclib.py
  :pyobject: helloLs

Measuring the message delay and throughput
==========================================

File `03-messaging.py <../../../demo/parallel/vm/03-messaging.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_

.. literalinclude:: ../demo/parallel/vm/03-messaging.py

The :func:`bounceBack` function is defined in the :mod:`funclib` module (file `funclib.py <../../../demo/parallel/vm/funclib.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_). 
This function bounces back every received message to its source. 

.. literalinclude:: ../demo/parallel/vm/funclib.py
  :pyobject: bounceBack

The output for communication between processes on the same host

.. code-block:: none

	Warning. Measuring local communication speed.
	Task layout:
	localhost ncpu=8 free slots: []
		slot=   0 task=   0
		slot=   1 task=   1

	Measuring message delivery time and data throughput to localhost.
	Bounce back task: 1:1
	localhost_2538_0 VM: Changing working directory to '/mnt/data/Data/pytest/demo/parallel/vm'.
	Data size     0.000kB, iterations= 10000, time=     37us, speed=0.000Mb/s
	Data size     0.001kB, iterations= 10000, time=     37us, speed=0.216Mb/s
	Data size     0.010kB, iterations=  2701, time=     38us, speed=2.118Mb/s
	Data size     0.100kB, iterations=  2647, time=     38us, speed=21.308Mb/s
	Data size     1.000kB, iterations=  2663, time=     40us, speed=199.249Mb/s
	Data size    10.000kB, iterations=  2490, time=     48us, speed=1661.765Mb/s
	Data size   100.000kB, iterations=  2077, time=    100us, speed=8023.758Mb/s
	Data size  1000.000kB, iterations=  1002, time=    755us, speed=10601.659Mb/s
	Data size 10000.000kB, iterations=   132, time=  12370us, speed=6467.453Mb/s
	calypso_2537_0 MPI: Task 1:1 exit detected.

Running and debugging the task
==============================

To start the nominal design task, select one of its items in the Design tasks 
tree and select task/Start locally from the main menu. The GUI will check the 
project and the task setup, dump it, and start the task. If it finds any error 
or inconsistency in the setup you will get an error message and the task won't 
be started. 

When the task is running, open the log by selecting Task/View log from the 
main menu. The task's progress is written to the log and the log tab will 
make it possible for you to follow it. For every circuit verification and 
every candidate circuit that improves the cost function the circuit's 
performance will be printed. 

.. figure:: gui-nominal-running-log.png
	:scale: 80%
	
	Viewing the log while the task is running. 
	
If your task does not behave as expected you can debug it by setting the 
debug level in the Output item of the task's setup to a nonzero value. 
Most common errors occur in the simulator module and the evalautor module. 
The former ones are usually caused by errors in the circuit's description, 
while the latter ones are mostly due to errors in performance measure 
definitions. The debug level of the simulator should be set to 3 or more 
so that the complete output of the simulator is written to the log file. 

Performance measures can be debugged by setting the debug level of the 
evaluator to a nonzero value. Level 1 will display diagnostic messages 
while level 2 will also print the values of the performance measures. 
For writing arbitrary messages to the log file you can use the ``m.debug()`` 
function in the definition of a performance measure. 

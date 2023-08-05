Task log tabs
=============

The log tab for the active task can be opened by selecting Task/View log 
in the main menu. Log tabs can be closed. They display the contents of 
a log file (which is a text file with particular structure). 

.. figure:: gui-log.png
	:scale: 80%
	
	A task log tab. 
	
In the top part of a log tab is the path to the log file and the timepoint 
when the log was created (timepoint of the first entry). Below this a group 
of checkboxes makes it possible to enable/disable the display of 
  
   * relative time of log entries with respect to log start
   * host where the log entries originates from 
   * local process IDs of the tasks that created the entries
   * local microthread IDs of the microthreads that created the entries
   * PyOPUS subsystem IDs specifying the subsystems that created the messages

The log can be scrolled. If the Tail checkbox is checked then the log jumps 
to its last entry whenever a new entry is detected in the log file. 

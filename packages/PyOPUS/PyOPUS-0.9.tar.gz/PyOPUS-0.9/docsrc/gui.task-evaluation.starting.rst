Starting the task
=================

You can define multiple tasks. One of them is the active task (displayed in 
the GUI window's status bar). To activate a task select one of its items in 
the Design tasks tab. 

The active task is started by selecting Task/Start locally in the main menu 
(or pressing ``F5``). When a task is started its status displayed in the 
window's status bar changes and some messages are printed in the part of the 
GUI window that displays messages. When the task is finished its status 
changes to "finished" and a message is printed. Messages for a succesfully 
started and finished task look like this. 

.. code-block:: none

   Preparing folder and files for running task 'evaluate'.
   Removing folder/file 'evaluate'.
   Dumping data.
   Task 'evaluate' starting in single process mode.
   Task 'evaluate' started.
   Task 'evaluate' finished.
   
First a folder is created with the name of the task and all files that 
are listed in the project are copied there. If the folder already exists 
a dialog is displayed with the warning that old results will be lost and 
asking you to confirm that you want to start the task. 

The project and the task's settings are dumped to a file titled ``runme.py`` 
in the tasks's folder. The file contains a short script that starts the task. 
This file is run with the Python interpreter and its text output is collected 
to a file named ``evaluate.log``. 

Before the project and the task's data are dumped to the ``runme.py`` file 
they are checked for consistency. If an error is found the process of dumping 
the data is interrupted and an error message is displayed. Suppose we have two 
design parameters in the task that have the same name. This is not allowed 
and will result in an error. 

.. figure:: gui-evaluation-run-error.png
	:scale: 80%
	
	An error is displayed if the data in the GUI is invalid or inconsistent. 

The tasks's folder contains files named ``lock.*``. These files are used by the 
GUI to detect the tasks's state. During the course of task's execution a 
subfolder named ``waveforms.pck`` is created. Here the waveforms obtained from 
the simulator are stored. Most of the files in this folder are named according 
to the following rule. 

.. code-block:: none

   <result node id>_<corner name>_<analysis name>.pck
   
Files named 

.. code-block:: none

   <result node id>_<corner name>.pck
   
contain the environments in which performance measures that do not belong to 
any particular analysis are evaluated. 

The result nodes holding various extracted information are stored in an 
SQLite database file in the task's folder. In our case this file is named 
``evaluate.sqlite``. 

If you want to interrupt the active task select Task/Stop from the main menu. 
Sometimes a task stays in the "running" state although the process is already 
dead. In that case you can manually switch it to "ready to be started" state 
by selecting "Task/Unlock" from the main menu. 

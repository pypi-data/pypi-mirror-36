Postprocessing setup file
=========================

The postprocessing setup (performance measures and plots for postprocessing) 
are stored in a text file named 

.. code-block:: none

   <task name>.post.json
   
The file is JSON encoded and human readable. Whenever you make a change in 
the postprocessign setup an asterisk will appear next to the title of the 
results tab. This means that the postprocessing setup is not saved. To save 
it select File/Save from the main menu. 

Every task has one results database file (named ``<task name>.sqlite``), one 
corresponding postprocessing setup file (named ``<task name>.post.json``), and 
one task folder (named ``<task name>``) where the task is run. The waveforms 
and the log are stored in the task folder. 

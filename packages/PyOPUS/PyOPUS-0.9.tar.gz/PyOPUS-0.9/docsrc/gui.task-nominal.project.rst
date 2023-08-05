Preparing the project
=====================

In the project we did not specify any performance measures. They are needed 
for evaluating the circuit's performance. Design requirements are imposed on 
the circuit's performance. The opptimizer compares the values of the 
performance measures to the design requirements and tries to update the design 
parameters in such manner that the design requirements are satisfied. 

First, open the ``simple.pog`` file in folder 
`demo/gui/miller/02-nominal/ <../../../demo/gui/miller/02-nominal/>`_
This project has an ``evaluate`` task  and a postprocessing setup that 
includes all of the performance measures defined for the Miller opamp in 
section :ref:`design-miller`. 

We start by copying the performance measures from the ``evaluate`` task's 
postprocessing setup to the Measures node of the project tree. In the Design 
tasks tree select the "evaluate" task. From main menu select Task/View results. 
In the results tab select all posprocessing measures, right-click the 
selection and select Copy from the context menu that appears. 

.. figure:: gui-nominal-copy-measures.png
	:scale: 80%
	
	Copying the performance measures from the postprocessing setup of the "evaluate" task. 

Next, in the Project tree select the Measures item, right-click it and 
select Paste from the popup menu. 

.. figure:: gui-nominal-paste-measures.png
	:scale: 80%
	
	Pasting the performance measures into the project. 
	
Now we have a bunch of performance measures of which most also have some 
design requirements impowed on them. You can get an overview of all 
performance measures defined in the project by selecting the Measures item 
in the Project tree. 

.. figure:: gui-nominal-project-measures.png
	:scale: 80%
	
	An overview of the performance measures defined and corresponding 
	design requirements defined in the project. 
	
It is now time to save this project in a different folder. Create a folder 
and save the project by selecting File/Save Project As in the main menu. 






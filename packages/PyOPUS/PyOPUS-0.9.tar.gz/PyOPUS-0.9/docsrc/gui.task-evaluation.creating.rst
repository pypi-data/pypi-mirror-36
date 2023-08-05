Creating a new evaluation task
==============================

Go to the Desing tasks tab and right-click the left part (Design tasks) 
where the tasks tree is displayed. Select "Add item after" from the 
context menu. A new task is created. Rename it to "evaluate" and expand 
its tree item. Task names must be unique identifiers. 

.. figure:: gui-evaluation-create.png
	:scale: 75%
	
	A newly created task for evaluating the circuit. 

You can add a description to the task. The Requirements item is empty 
because we are not going to design the circuit. We are only evaluating 
it. Select the Parameters item. The Design parameters from the project 
were automatically copied. The task allways uses the values specified here 
instead of those specified in the project. We deleted the lower and the 
upper bound on the parameter values because they are not needed for circuit 
evaluation. There is nothing to do here. If, however, you want to use 
different values for the design parameters you can enter them here. 

.. figure:: gui-evaluation-params.png
	:scale: 75%
	
	The design parameters setup is automatically copied from the 
	project to the newly created task. 

A corner is a combination of operating parameters and device models. Usually 
a corner describes some extreme combination of operating conditions and 
device models. We expect the circuit's performance measures to reach their 
extreme valus in corners. When we crated the evaluation task a "nominal" 
corner was automatically created. The "nominal" corner comprises nominal 
operating parameter values. Because when we were defining analyses we did not 
specify the MOS transistor model we must specify it in the "nominal" corner 
definition. We are going to use the typical model defined in input module 
"tm". 

Expand the Corners item and select the nominal corner. Nw yopu can edit its 
properties. As you can see the nominal values of operating parameters and 
zeros for statistical parameters were automatically added to the corner's 
settings. All we need to do is to add the "tm" input module to the Input 
modules table. 

.. figure:: gui-evaluation-corner-nominal.png
	:scale: 75%
	
	Adding the "tm" input module to the "nominal" corner. 

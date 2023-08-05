Opening and browsing the results
================================

As soon as the task is started it begins to generate intermediate results and 
stores them in a file ``evaluate.sqlite`` in the project folder which is a 
sqlite database. The results database of the active task can be opened by 
selecting Task/View results in the main menu. This opens a tab which displays 
the contents of the database in form of a tree. 

.. figure:: gui-post-task-project.png
	:scale: 75%
	
	GUI displaying the results database of the simple evaluation task. 
	The "evaluate" task node's project aspect is displayed in the right half of the tab. 

The top of the results tab displays the path to the database file and the 
timepoint when the database was created. The display is updated as new data is 
added to the database. The database is organized as a tree. Every node in the 
tree can have one or more aspects holding various data. The tree is displayed 
in the left part of the tab (Results database). The available aspects, 
posprocessing performance measures, and postprocessing plots for the selected 
result node are listed in the middle part of the tab (Postprocessing). The 
data corresponding to the selected aspect are displayed in the right part of 
the tab. 

The top of the aspect display lists the result node ID, type, and time the 
node was created (relative to log start). In some cases there is also a checkbox 
titled "Text mode". When checked the results are displayed as text. 

Our results database has 4 result nodes. The first one (evaluate) holds the 
task definition. It has two aspects (project and task). They are JSON 
encoded descriptions of the project and task dumped to the ``runme.py`` file. 

The Aggregator setup node holds no data. This is due to the fact that we 
did not define any performance measures and consequently haven't set any 
design requirements based on these measures. 

The "Pass 1 verification" node (which is an optimization iteration node) 
holds the actual results of the circuit evaluation. It has three aspects 
(parameters, performance, and cost). The performance and cost apects are 
empty because we did not define any performance measures is the project/task. 
The parameters aspect holds the values of the design parameters for which the 
circuit was evaluated. 

.. figure:: gui-post-iter-param.png
	:scale: 75%
	
	The design parameter values stored in an optimization iteration node. 

.. figure:: gui-post-iter-param-text.png
	:scale: 75%
	
	The design parameter values displayed as text. 

The task summary node is the last node in the tree. It holds some stats on 
the task like the number of performed analyses and the task's duration. 

.. figure:: gui-post-summary.png
	:scale: 75%
	
	The task summary node. 

For every result node in the database a set of waveforms is possibly stored 
by PyOPUS in the ``waveforms.pck`` subfolder of the task folder. To see if 
any waveforms are available select the "Result aspects" node in the 
Postprocessing tree. A list of waveform files is displayed in the right half 
of the tab. 

.. figure:: gui-post-iter-pckfiles.png
	:scale: 75%
	
	Viewing the list of available waveform files. 
	

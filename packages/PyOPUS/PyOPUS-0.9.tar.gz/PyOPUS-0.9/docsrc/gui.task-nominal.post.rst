Postprocessing saved waveforms
==============================

We don't have any postprocessing performance measures nor plots defined for
task "nominal". We are going to copy them from the postprocessing setup of 
task "evaluate". Select any item under the "evaluate" task and choose 
Task/View results from the main menu. A new tab with the results of the 
"evaluate" task and its postprocessing setup will appear. 

Select all defined plots in the Postprocessing tree, right-click the 
selection, and choose Copy from the context menu. 

.. figure:: gui-nominal-post-copy.png
	:scale: 70%
	
	Copying the plots from the postprocessing setup of the "evaluate" task. 

Then go to the tab 
displaying the results of the "nominal" task, select the "Plots (post)" item 
in the Postprocessing tree, right-click it and select Paste from the context 
menu. Now all the plots set up in the "evaluate" task's results are copied to 
the postprocessing setup of the "nominal" task's results. You can use them 
to display the waveforms stored during the nominal design task. 

.. figure:: gui-nominal-post-paste.png
	:scale: 70%
	
	Pasting the plots into the postprocessing setup of the "nominal" task. 
	
Of all the result nodes only the initial circuit evaluation (Pass 1 
verification) and the final circuit evaluation (Pass 2 verification) have 
available waveforms. Select the initial circuit evaluation node and click on 
the CMRR plot in the Postprocessing tree. The CMRR response of the initial 
circuit is plotted. To make the plot bigger you can hide the top right and 
the bottom pane of the display by moving the splitters. 

.. figure:: gui-nominal-post-cmrr1.png
	:scale: 70%
	
	Viewing the CMRR response of the initial circuit. 

To view the CMRR response of the final circuit you simply select the final 
circuit evaluation node in the Results database. The CMRR plot for the 
final circuit is displayed. 

.. figure:: gui-nominal-post-cmrr2.png
	:scale: 70%
	
	Viewing the CMRR response of the final circuit.
	
Just like you can define plots for postprocessing, you can also define 
performance measures. See section :ref:`gui-post-measures` for more 
information on how to do this. 

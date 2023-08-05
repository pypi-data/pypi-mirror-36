Task settings
=============

What we created in this section is an evaluation/corner design task. What the 
task does depends on the optimization method which is set under the Task 
settings tree item. By default it is set to "Evaluate only (all corner-analysis pairs)". 
This means that the circuit will be evaluated for all possible corner-analysis 
pairs. 

Beside this default method another type of evaluation is available - 
"Evaluate only (required corner-analysis pairs)". This method evaluates only 
those corner-analysis pairs for which there is a performance measure defined. 
In our case we have no performance measures so no corner-analysis pair 
will be evaluated and no waveforms will be produced. Therefore this second 
method is not appropriate for us. 

.. figure:: gui-evaluation-settings.png
	:scale: 75%
	
	Task settings for Miller opamp evaluation. 

Other optimization methods are not used for evaluating the circuit. Typically 
you use them to search for design parameter values for which the performance 
measures satisfy all design requirements across the set of defined corners. 
We are going to explain them in later sections. 

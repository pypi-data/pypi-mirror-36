.. _tut-evaluation-plotter:

Plotting simulation results
===========================

This demo shows how to use the :class:`pyopus.visual.wxmplplotter.WxMplPlotter` 
class for plotting the simulation results. Read the :ref:`tut-evaluation-evaluator` 
chapter to learn more about the :class:`pyopus.evaluator.performance.PerformanceEvaluator` class. 

The problem definition in the main file 
`runme.py <../../../demo/evaluation/03-plotter/runme.py>`_ in folder 
`demo/evaluation/03-plotter/ <../../../demo/evaluation/03-plotter/>`_
is identical to the one in chapter :ref:`tut-evaluation-evaluator`. 
Only the differences are given in this document. 

First we must import the plotter and the MatPlotLib wrapper. 

.. literalinclude:: ../demo/evaluation/03-plotter/runme.py
	:start-after: # Plotter import
	:end-before: # End plotter import

We add a common mode DC sweep to the analyses (`dccom`). 

.. literalinclude:: ../demo/evaluation/03-plotter/runme.py
	:start-after: # Analyses
	:end-before: # End analyses
	
Everything we want to plot must be collected by the evaluator. Therefore 
we add some mesurements that result in vectors from which we draw the x-y 
data for the plots (measures `dcvin`, `dcvout`, `dccomvin`, `dccomvout`, and 
`dccom_m1vdsvdsat`). 

.. literalinclude:: ../demo/evaluation/03-plotter/runme.py
	:start-after: # Measures
	:end-before: # End measures

Now we define the plots for the plotter. 

.. literalinclude:: ../demo/evaluation/03-plotter/runme.py
	:start-after: # Visualisation
	:end-before: # End visualisation

Finally we put it all together in the main program. 

.. literalinclude:: ../demo/evaluation/03-plotter/runme.py
	:start-after: # End visualisation

.. image:: tutorial.evaluation.03-plotter-1.png
	:scale: 75%
	
.. image:: tutorial.evaluation.03-plotter-2.png
	:scale: 75%
	

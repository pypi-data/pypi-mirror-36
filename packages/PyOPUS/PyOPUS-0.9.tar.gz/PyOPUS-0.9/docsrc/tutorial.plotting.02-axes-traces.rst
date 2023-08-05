Adding axes and traces to plot windows
======================================

First the MatPlotLib GUI must be locked. This disables refreshing and avoids race conditions between threads. 
After verifying that the plot window is still there (if it is not, API calls will crash) the axes and the 
traces are added using the MatPlotLib API. In the end the figure is drawn and the GUI is unlocked. 

Make sure that all the arrays you plot (and all other data) is accessed only by MatPlotLib after it has been 
plotted. If you are not sure, pass a copy of the data to the API calls (so that after plotting you can still 
mess around with the original data without crashing the GUI). 

File `02-axes-traces.py <../../../demo/plotting/02-axes-traces.py>`_ 
in folder `demo/plotting/ <../../../demo/plotting>`_

.. literalinclude:: ../demo/plotting/02-axes-traces.py
   
.. image:: tutorial.plotting.02-axes-traces-1.png
	:scale: 75%

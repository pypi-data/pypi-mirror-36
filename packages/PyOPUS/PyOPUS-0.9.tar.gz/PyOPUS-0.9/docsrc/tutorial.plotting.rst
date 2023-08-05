Plotting facilities in PyOPUS
=============================

This tutorial explains how to use the MatPlotLib wrapper. This wrapper makes it possible 
for your scripts to run while all the plots remain responsive. 

The main steps of the tutorial involve opening a plot window, creating axes (subplots), 
plotting simple x-y traces, logarithmic and polar plots, setting the aspect ratio and 
scaling a plot, adding annotations (i.e. grid, legend, text), and storing a plot in a 
file for inclusion in your documents. An example creating a 3D plot is also given. 

Most of the MatPlotLib capabilities are accessible via the MatPlotLib API once a plot 
window is created. The major difference is that you must lock the display before you 
make any changes to the plots. Once you are finished making shanges the display can 
be unlocked and the plots become responsive again. 

One thing to keep in mind is that any data passed to MatPlotLib must be left untouched 
by the rest of your program. To achieve this make sure all the data you pass to 
MatPlotLib is a copy of your original data that you may modify at some later point. 
If you fail to do this your program may crash. 

.. toctree::
   :maxdepth: 2
   
   tutorial.plotting.01-windows.rst
   tutorial.plotting.02-axes-traces.rst
   tutorial.plotting.03-subplot.rst
   tutorial.plotting.04-manual-subplot.rst
   tutorial.plotting.05-logplot.rst
   tutorial.plotting.06-scaling.rst
   tutorial.plotting.07-polar-aspect.rst
   tutorial.plotting.08-grid-annotations.rst
   tutorial.plotting.09-file-output.rst
   tutorial.plotting.10-3d.rst
   
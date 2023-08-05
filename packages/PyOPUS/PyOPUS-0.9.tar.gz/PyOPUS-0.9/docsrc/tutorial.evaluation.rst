.. _tut-evaluation:

Simulators and result evaluation
================================

This tutorial demonstrates how to use the simulator interface, how to extract performances from 
simulation results, and how to plot the simulation results without doing all of the cumbersome 
MatPlotLib stuff. It also demonstrates how to construct an aggregate cost function from the 
evaluated performances. The resulting const function can then be minimized with an arbitrary 
optimization algorithm to find a better circuit. The response of the circuit can be plotted 
during an optimization run so one can see how the circuit is improving. 

.. toctree::
   :maxdepth: 2
   
   tutorial.evaluation.01-simulator-spiceopus.rst
   tutorial.evaluation.01-simulator-hspice.rst
   tutorial.evaluation.01-simulator-spectre.rst
   tutorial.evaluation.02-evaluator.rst
   tutorial.evaluation.03-plotter.rst
   tutorial.evaluation.04-cost.rst
   tutorial.evaluation.05-optimize.rst
   tutorial.evaluation.06-iteration-plotter.rst
   
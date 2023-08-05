Task settings
=============

Under Task settings you can set up the task's behavior. The optimizer tries to 
find a better circuit by minimizing a so-called cost function. The penalty 
that is added to the cost function is set under "Penalty for failed measures". 
This should be a large value so that the optimizer avoids circuits that can't 
be evaluated. 

If "Stop when all requirements are satisfied" is checked the optimizer will 
stop as soon as it finds a circuit that satisfies all design requirements. 
If unchecked the optimizer runs until it reaches the limit on the number of 
evaluated candidate circuits or until it converges. This can take a 
significant amount of time and does not neccessarily produce a better result. 

If you specify at least one tradeoff weight in the definition of design 
requirements under the Requirements item and set the "Tradeoff weight multiplier" 
to a nonzero value the optimizer will try to improve the circuit beyond the 
specified design requirements for those performance measures for which you 
specified a tradeoff weight. This is acieved by adding a negative penalty to 
the cost function for every circuit that exceeds the design requirements. The 
"Tradeoff weight multiplier" specifies how large this reward should be. Usually 
you set it to a value much smaller than one (i.e. 1e-3) because the optimizer 
should primarily satisfy the design requirements and not try to improve the 
circuit beyond them untill all of them are satisfied. It makes sense to 
uncheck the "Stop when all requirements are satisfied" option if you set 
the tradeoff weight multiplier to a nonzero value. 

There are several optimization methods available. 

   * PSADE - a global method based on simulated annealing and 
     differential evolution
   * Differential evolution - a global optimization method
   * QPMADS - a local optimization method based on quadratic models and 
     mesh adaptive direct search
   * Box's constrained simplex - a local method, an extension of the 
     Nelder-Mead simplex method that supports constraints. 
   * Hooke-Jeeves - a local method from the family of pattern search 
     algorithms

Addittionally two methods that only evaluate the circuit for the initial 
values of the design parameters are available. 

   * Evaluate only (required corner-analysis pairs) - evaluated only those 
     corner-analysis pairs for which a performance measure is defined and 
     at least one design requirement (above/below) is imposed. 
   * Evaluate only (all corner-analysis pairs) - evaluates all available
     corner-analysis pairs. Useful for generating wavefors that are used for 
     initially setting up the performance measures in the postprocessing 
     section of the results tab. This is the default setting when you create 
     an evaluation/corner-based design task. 

.. figure:: gui-nominal-task-settings.png
	:scale: 80%
	
	Task settings. 

Optimization is performed in mutiple passes (i.e. multiple consecutive 
runs of an optimization algorithm). The upper limit for the number of 
evaluated candidate circuits per pass is exactly what you expect it to be. 
It sets the ``maxiter`` parameter of the optimization algorithm. 

The "Initial step" and "Stop when step is smaller than" are for setting 
the optimizer's initial step and the step-based stopping condition. These 
two values translate to parameters passed to the constructor of the 
optimization algorithm. 

   * PSADE - the two settings are not passed
   * Differential evolution - the two settings are not passed
   * QPMADS - the two settings are passed as the ``startStep`` and the 
     ``stopStep`` parameters
   * Box's constrained simplex - the first setting is ignored and the 
     second one is passed as the ``gamma_stop`` argument
   * Hooke-Jeeves - the two settings are passed as the ``step0`` and the 
     ``minstep`` parameters

Checking "Use solution from previous pass as initial point" uses the 
solution of the last completed optimization pass as the initial point for 
the next pass. The initial point for the first pass is defined with the 
initial values of the design parameters. 

Checking "Use only relevant corners in optimization" enables the iterative 
algorithm for finding the corners where worst values of performance measures 
take palce. If unchecked every candidate circuit is evaluated across all 
corners which can be very expensive if you define many corners. 

Finally, there tables "Evaluator settings", "Aggregator settings", and 
"Optimizer settings" allow you to specify arbitrary parameters for the 
constructors of :mod:`pyopus.evaluator.performance.PerformanceEvaluator`, 
:mod:`pyopus.evaluator.aggregate.Aggregator`, and the optimizer algorithm. 
You can use hash expressions for the values in these tables. 

.. figure:: gui-nominal-task-output.png
	:scale: 80%
	
	Output settings of a task. 

Under the Output item you can specify what will be written to the log file 
and which waveforms will be stored. Debug levels can be specified for 
various PyOPUS components. A debug level of zero meand no debug messages 
are written to the log. Higher levels result in more verbosity. The debug 
level can be set for the simulator, the evaluator, the aggregator, the 
optimizer, and the task itself. By default the task's debug level is set 
to 1 so that you can monitor the task's progress in the log. 

Enabling "Keep intermediate files on disk" will keep all simulator input 
and output files on disk. Normally these files are deleted once a circuit 
is evaluated and the waveforms are collected. 

Enabling "Save results for all evaluated circuits" will create a node in 
the results database for every evaluated circuit. Normally the results are 
stored only for circuits that improve the value of the cost function. 

The "Save waveforms" selector specified for which circuits the waveforms 
will be stored. It has three options. 

   * Never
   * Only for verification across corners (default)
   * For every saved results
   
The second option saves the waveforms for circuit verification that takes 
place in in the beginning and the end of the task, and between optimization 
passes. 

.. _tut-evaluation-cost:

Constructing an aggregate cost function
=======================================

This demo shows how to use the :class:`pyopus.evaluator.aggregate.Aggregator` 
class for constructing an aggregate cost function from the results collected 
by a performance evaluator. Read chapter :ref:`tut-evaluation-evaluator` 
to learn more about the :class:`pyopus.evaluator.performance.PerformanceEvaluator` 
class. 

First we leave most parameters to be set by PyOPUS. Therefore we remove their default 
values from the definition of the amplifier in file 
`opamp.inc <../../../demo/evaluation/04-cost/opamp.inc>`_ in folder 
`demo/evaluation/04-cost/ <../../../demo/evaluation/04-cost/>`_

.. literalinclude:: ../demo/evaluation/04-cost/opamp.inc

The problem definition in the main file 
`runme.py <../../../demo/evaluation/04-cost/runme.py>`_ in folder 
`demo/evaluation/04-cost/ <../../../demo/evaluation/04-cost/>`_
is identical to the one in chapter :ref:`tut-evaluation-plotter`. 
Only the differences are given in this document. 

First we import the the things we need. 

.. literalinclude:: ../demo/evaluation/04-cost/runme.py
	:start-after: # Imports
	:end-before: # End imports

We define the parameter values. 

.. literalinclude:: ../demo/evaluation/04-cost/runme.py
	:start-after: # Parameters
	:end-before: # End parameters

Because the input for an aggregate cost function is a parameter vector we 
must specify the order in which the parameters are placed in this vector. 
We simply take the keys of the parameters dictionary and sort them. 

.. literalinclude:: ../demo/evaluation/04-cost/runme.py
	:start-after: # Parameter order
	:end-before: # End parameter order

Next we define the aggregate cost function components. The function value 
is obtained by summing all of the components. Every component is 
based on some performance measure collected by the performance evaluator. 
The aggregate cost function reflects the quality of the circuit. 
Lower values should correspond to better circuits. 

.. literalinclude:: ../demo/evaluation/04-cost/runme.py
	:start-after: # Definition
	:end-before: # End definition
	
Finally we put it all together in the main program. 

.. literalinclude:: ../demo/evaluation/04-cost/runme.py
	:start-after: # Main program

This is the output we get (debug output is omitted)

.. code-block:: none

  cost=1.190359e+01
            dif_l:    1.080000e-06
            dif_w:    7.730000e-06
           load_l:    2.570000e-06
           load_w:    3.486000e-05
           mirr_l:    5.600000e-07
           mirr_w:    7.456000e-05
            out_l:    3.800000e-07
            out_w:    4.801000e-05
        isup  <  1.000e-03    | .    1.112e-03     worst_power : 0
      out_op  <  1.000e+01    |      1.004e+00     worst_power : 0
     vgs_drv  >  1.000e-03    | o   -1.046e-02         nominal : 11.5
     vds_drv  >  1.000e-03    |      1.026e-01     worst_speed : 0
       swing  >  1.600e+00    | o    1.449e+00     worst_speed : 0.0944
   mirr_area  <  8.000e-10    | o    8.351e-10         nominal : 0.351
  
  Analysis count: {'dccom': 5, 'dc': 5, 'op': 5}
  
The aggregate cost if printed along with the parameter values. 

For every aggregate cost component the corresponding requirement is printed. 
Dots denote components that fail to satisfy requirements but are not included 
in the aggregate cost. Symbol 'o' denotes components that are included and 
fail to satisfy the requirement. For every component the value of the 
performance is printed along with the corner where the worst performance is 
observed and the contribution to the aggregate cost. Note how performances 
that satisfy the requirements produce contributions that are not greater than 0. 
Finally, the analysis count is printed. 

Note that debug output can be disabled by setting the *debug* parameter to 0. 

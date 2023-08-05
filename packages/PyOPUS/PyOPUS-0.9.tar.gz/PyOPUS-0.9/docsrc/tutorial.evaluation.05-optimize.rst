.. _tut-evaluation-optimize:

Optimizing a circuit
====================

This demo shows how to optimize the circuit by minimizing an aggregate cost
function. Read chapter :ref:`tut-evaluation-cost` to learn more about the 
:class:`pyopus.evaluator.aggregate.Aggregator` class. 

The problem definition in the main file 
`runme.py <../../../demo/evaluation/05-optimize/runme.py>`_ in folder 
`demo/evaluation/05-optimize/ <../../../demo/evaluation/05-optimize/>`_
is identical to the one in chapter :ref:`tut-evaluation-cost`. 
Only the differences are given in this document. 

First we import the the things we need. 

.. literalinclude:: ../demo/evaluation/05-optimize/runme.py
	:start-after: # Imports
	:end-before: # End imports

For every parameter we define the bounds (low and high) and the initial values. 

.. literalinclude:: ../demo/evaluation/05-optimize/runme.py
	:start-after: # Input parameters
	:end-before: # End input parameters

We choose an ordering for the parameters so that we can form parameter vectors. 

.. literalinclude:: ../demo/evaluation/05-optimize/runme.py
	:start-after: # Parameter order
	:end-before: # End parameter order

The optimization is invoked in the main program. We perform it with the 
Hooke-Jeeves optimizer. We limit the number of circuit evaluations to 1000. 

.. literalinclude:: ../demo/evaluation/05-optimize/runme.py
	:start-after: # Main program

This is the output we get after the optimization is finished

.. code-block:: none

  Final cost: -0.00175869779887, found in iter 47, total 47 iteration(s)
            dif_l:    1.462000e-06
            dif_w:    7.730000e-06
           load_l:    3.716000e-06
           load_w:    1.606000e-05
           mirr_l:    5.600000e-07
           mirr_w:    5.576000e-05
            out_l:    1.800000e-07
            out_w:    6.681000e-05
        isup  <  1.000e-03    | .    1.106e-03     worst_power : 0
      out_op  <  1.000e+01    |      1.009e+00     worst_power : 0
     vgs_drv  >  1.000e-03    |      4.457e-03         nominal : 0
     vds_drv  >  1.000e-03    |      6.339e-02     worst_speed : 0
       swing  >  1.500e+00    |      1.506e+00     worst_speed : -3.82e-06
   mirr_area  <  8.000e-10    |      6.245e-10         nominal : -0.00175
  
  Performance in corners
   mirr_area |         nominal:    6.245e-10
        isup |         nominal:    1.079e-03
             |     worst_power:    1.106e-03
             |     worst_speed:    1.063e-03
      out_op |         nominal:    9.363e-01
             |     worst_power:    1.009e+00
             |     worst_speed:    9.093e-01
     vgs_drv |         nominal: [ 0.24441163  0.26256044  0.00445736]
             |     worst_power: [ 0.30278812  0.30734632  0.0101956 ]
             |     worst_speed: [ 0.32222824  0.32687977  0.01898317]
             |       worst_one: [ 0.30044591  0.30543455  0.01019236]
             |      worst_zero: [ 0.32116742  0.32542464  0.0189832 ]
     vds_drv |         nominal: [ 1.12073222  0.4485023   0.1022935 ]
             |     worst_power: [ 0.8711309   0.52563123  0.22122619]
             |     worst_speed: [ 0.69354036  0.30536617  0.06339319]
             |       worst_one: [ 0.62915635  0.22867587  0.1455108 ]
             |      worst_zero: [ 0.81162835  0.48450811  0.06420577]
       swing |         nominal:    1.555e+00
             |     worst_power:    1.721e+00
             |     worst_speed:    1.506e+00
             |       worst_one:    1.509e+00
             |      worst_zero:    1.520e+00
  
  
  Analysis count: {'op': 240, 'dc': 240, 'dccom': 240}
  

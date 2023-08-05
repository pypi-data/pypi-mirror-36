.. _tut-evaluation-evaluator:

Using the performance evaluator
===============================

This demo shows how to use the :class:`pyopus.evaluator.performance.PerformanceEvaluator` class for 
generating the simulator jobs and evaluating the collected simulation results. 
Read chapter :ref:`tut-evaluation-spiceopus` to learn about the sample 
circuit and the device model files. The example uses the SPICE OPUS circuit 
simulator. 

The circuit description is split in two files. The ``demo/evaluation/02-evaluator/opamp.inc`` 
file contains the definition of the Miller opamp subcircuit. 

.. literalinclude:: ../demo/evaluation/02-evaluator/opamp.inc
   :language: none

File ``demo/evaluation/02-evaluator/topdc.inc`` contains the testbench circuit 
surrounding the opamp. This circuit is used for evaluating the opamp's 
performance.

.. literalinclude:: ../demo/evaluation/02-evaluator/topdc.inc

File: ``demo/evaluation/02-evaluator/runme.py``

.. literalinclude:: ../demo/evaluation/02-evaluator/runme.py

This is the output we get (excluding debug output)

.. code-block:: none

          mirr_w:    7.460000e-05
          mirr_l:    5.630000e-07
  mirr_area |         nominal:    8.400e-10
       isup |         nominal:    1.078e-03
            |     worst_power:    1.111e-03
            |     worst_speed:    1.068e-03
     out_op |         nominal:    9.035e-01
            |     worst_power:    1.004e+00
            |     worst_speed:    9.041e-01
    vgs_drv |         nominal: [ 0.20979231  0.21155576 -0.01015429]
            |     worst_power: [ 0.25183658  0.25389873 -0.00648101]
            |     worst_speed: [ 0.26954062  0.2716014   0.00189362]
            |       worst_one: [ 0.25043159  0.25257277 -0.00648411]
            |      worst_zero: [ 0.26837357  0.27032976  0.00189365]
    vds_drv |         nominal: [ 0.81923904  0.70281508  0.12600147]
            |     worst_power: [ 0.93198506  0.80043261  0.25860023]
            |     worst_speed: [ 0.7543191   0.61157677  0.10224135]
            |       worst_one: [ 0.68953021  0.5430789   0.1819348 ]
            |      worst_zero: [ 0.87452691  0.74942676  0.10313849]
      swing |         nominal:    1.486e+00
            |     worst_power:    1.661e+00
            |     worst_speed:    1.450e+00
            |       worst_one:    1.454e+00
            |      worst_zero:    1.463e+00
  
  Analysis count: {'dc': 5, 'op': 5}
  Isup in nominal corner: 1.078055e-03

First the parameter values are printed followed by the performance measure values. 
The values are printed for all corners where a performance measure was evaluated. 
Finally the analyssi count is printed along with the manually picked performance 
(Isup in nominal corner). 

Note that debug output can be turned off by setting the *debug* parameter to 0. 

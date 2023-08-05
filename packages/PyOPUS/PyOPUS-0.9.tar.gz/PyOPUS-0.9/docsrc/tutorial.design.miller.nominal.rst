.. _design-miller-nominal:


Nominal design 
==============

We are going to find the values of design parameters for which the design 
requirements specified in `definitions.py <../../../demo/design/miller/definitions.py>`_ 
are satisfied at nominal operating conditions and with the typical process 
variation MOS models. The script is in file 
`02-nominal-design.py <../../../demo/design/miller/02-nominal-design.py>`_ 
in folder `demo/design/miller/ <../../../demo/design/miller/>`_

.. literalinclude:: ../demo/design/miller/02-nominal-design.py
   :language: python

The script first prepares dictionaries with nominal statistical parameter 
values (0), nominal operating parameter values and initial design parameter 
values. The nominal corner named ``nom`` is defined. This corner adds the 
'tm' module to the input netlist for the simulator and specifies the nominal 
values of operating parameters. 

Next, the cooperative multitasking OS is initialized. It uses MPI as the 
backend and starts every task in its own local folder which contains 
the copies of all files from the current folder (mirrorMap argument
to MPI). 

A :class:`pyopus.design.cbd.CornerBasedDesign` object is created from 
``designParams``, ``heads``, ``analyses``, ``measures``, ``variables`` 
defined in 
`definitions.py <../../../demo/design/miller/definitions.py>`_
and the ``corners`` variable constructed in this script. The bounds on 
design parameters are apecified in the ``designParams`` variable. The 
``fixedParams`` argument specifies the nominal statistical parameter 
values. These parameters do not change during optimization. The initial 
design is specified with the ``initial`` argument. For the process of 
optimization the ``global`` method is used (parallel SADE optimizer). 
The ``debug`` argument makes the optimizer print its progress during 
optimization. 

The design requirements are specified in the ``measures`` variable 
with ``lower`` and ``upper`` members of the dictionary describing 
a performance measure. Only performance measures for which at least one 
of these two values is specified will be subject to optimization. 

For the ``area`` performance measure the value of the norm is specified 
with the ``norms`` argument. In our case 1 penalty will be assigned 
for every 100um2 above the target value for the area. For other 
performance measures the norm is equal to the absolute value of the 
respetive ``lower`` or ``upper`` design requirement. If both of these 
requirements are specified the greater absolute value of both is used. 
If a norm is zero it is set to one. 

The optimization can be run in parallel on 5 local CPUs by typing 

.. code-block:: none

  mpirun -n 5 python3 02-nominal-design.py

The parallelization will happen at the optimizer level where multiple 
candidate solutions will be evaluated in parallel. 
Of the 5 CPUs one will be the master and the remaining 4 will be workers. 
This means that we can expect a speedup of up to 4. One can also include 
CPUs of remote machines in the process of optimization. Read the 
:ref:`parallel-vm` and the :ref:`parallel-cooperative` tutorials on how 
to do this. 

During optimization messages are printed that show the progress of the 
optimizer. When the optimization is finished the values of the design 
parameters obtained by the optimizer are printed

.. code-block:: none

          c_out:    4.496976e-12
         diff_l:    3.237868e-06
         diff_w:    1.541743e-05
         load_l:    3.077559e-06
         load_w:    5.160282e-05
         mirr_l:    2.677943e-06
        mirr_ld:    3.758176e-06
         mirr_w:    5.644932e-05
        mirr_wd:    8.414813e-06
        mirr_wo:    3.312984e-05
          out_l:    1.272839e-06
          out_w:    1.719281e-05
          r_out:    2.216717e+04

followed by the circuit's performance. 

.. code-block:: none

        area  <  9.000e-09    |      1.448e-09    nom : 0
        cmrr  >  9.000e+01    |      1.288e+02    nom : 0
        gain  >  6.000e+01    |      8.015e+01    nom : 0
        isup  <  1.000e-03    |      1.703e-04    nom : 0
    overshdn  <  1.000e-01    |      1.540e-03    nom : 0
    overshup  <  1.000e-01    |      1.538e-02    nom : 0
          pm  >  5.000e+01    |      8.152e+01    nom : 0
    psrr_vdd  >  6.000e+01    |      7.855e+01    nom : 0
    psrr_vss  >  6.000e+01    |      9.414e+01    nom : 0
      slewdn  >  2.000e+06    |      2.292e+06    nom : 0
      slewup  >  2.000e+06    |      2.272e+06    nom : 0
       swing  >  1.000e+00    |      1.218e+00    nom : 0
      tsetdn  <  1.000e-06    |      4.325e-07    nom : 0
      tsetup  <  1.000e-06    |      4.100e-07    nom : 0
        ugbw  >  1.000e+07    |      2.530e+07    nom : 0
     vds_drv  >  0.000e+00    |      1.498e-01    nom : 0
     vgs_drv  >  0.000e+00    |      6.355e-02    nom : 0

In the left half of the printout the design requirements are 
summarized. The first column of the right half lists the obtained 
circuit's performance followed by the corner where this performance 
was obtained and the penalty contribution to the final value of the 
cost function. Because all design requirements are satisfied all 
penalty contributions are 0. 

Note that due to the random nature of the delays on the network 
parallel runs may yield different solutions for the same design 
problem.

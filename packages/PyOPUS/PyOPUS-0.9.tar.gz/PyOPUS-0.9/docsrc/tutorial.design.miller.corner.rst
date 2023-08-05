.. _design-miller-corner:

Design across multiple corners
==============================

We are going to find the values of design parameters for which the design 
requirements specified in `definitions.py <../../../demo/design/miller/definitions.py>`_ 
are satisfied across multiple operating conditions and process variation 
MOS models. The script is in file 
`03-corner-based-design.py <../../../demo/design/miller/03-corner-based-design.py>`_ 
in folder `demo/design/miller/ <../../../demo/design/miller/>`_

.. literalinclude:: ../demo/design/miller/03-corner-based-design.py
   :language: python

After preparing dictionaries with statistical parameter values, nominal 
operating parameter values, and initial design parameter values the 
dictionary holding the corners is built (``generateCorners``). A total 
of 16 corners are generated (combinations of 2 supply voltages, 2 operating 
temperatures, and 4 MOS models). The name of a corners reflect the 
combination of parameters and model). The nominal corner is constructed 
manually and added to the dictionary. The corner name is composed as 

.. code-block:: none

  c<corner number>_<MOS model name>_<vdd value name>_<temperature value name>


The evaluation of the ``area`` performance measure is limited to the 
nominal corner by adding an entry named ``corners`` to the dictionary 
describing it. 

Next, the cooperative multitasking OS is initialized. It uses MPI as the 
backend and starts every task in its own local folder which contains 
the copies of all files from the current folder (mirrorMap argument
to MPI). 

A :class:`pyopus.design.cbd.CornerBasedDesign` is created from 
``designParams``, ``heads``, ``analyses``, ``measures``, ``variables`` 
defined in 
`definitions.py <../../../demo/design/miller/definitions.py>`_
and the ``corners`` variable constructed in this script. The setup is 
essentially the same as for nominal design, with the exception of the 
``incrementalCorners`` argument which turns on the iterative algorithm 
for finding the worst corner. Without this algorithm every candidate
circuit measure must be evaluated across all corners which can take 
a lot of time. 

It is recommended that you run this case with multiple CPUs. To run it 
in parallel on 5 local CPUs by typing 

.. code-block:: none

  mpirun -n 5 python3 03-corner-based-design.py

During optimization messages are printed that show the progress of the 
optimizer. First, the initial design is evaluated across all corners. 
For this example we start with the result obtained with the previous 
example (nominal design). We can see that two design requirements 
(cmrr>90 and pm>50) are not satisfied in some corners. The names of 
corners with the worst values of individual performance measures are 
printed alongside with the contributions to cost function value. 

.. code-block:: none

  calypso_7b2b_1 CBD: Pass 1, full corner evaluation
  calypso_7b2b_1 CBD: Pass 1, corner summary
  calypso_7b2b_1 CBD:         area  <  9.000e-09    |      1.448e-09    nom : 0
  calypso_7b2b_1 CBD:         cmrr  >  9.000e+01    | o    8.059e+01 c10_wo_vl_th : 0.105
  calypso_7b2b_1 CBD:         gain  >  6.000e+01    |      7.903e+01 c1_wp_vl_tl : 0
  calypso_7b2b_1 CBD:         isup  <  1.000e-03    |      1.709e-04 c3_wp_vh_tl : 0
  calypso_7b2b_1 CBD:     overshdn  <  1.000e-01    |      2.537e-03 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:     overshup  <  1.000e-01    |      2.219e-02 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:           pm  >  5.000e+01    |      6.368e+01 c3_wp_vh_tl : 0
  calypso_7b2b_1 CBD:     psrr_vdd  >  6.000e+01    |      7.290e+01 c10_wo_vl_th : 0
  calypso_7b2b_1 CBD:     psrr_vss  >  6.000e+01    |      8.496e+01 c5_ws_vl_tl : 0
  calypso_7b2b_1 CBD:       slewdn  >  2.000e+06    |      2.182e+06 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:       slewup  >  2.000e+06    |      2.133e+06 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:        swing  >  1.000e+00    |      1.007e+00 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:       tsetdn  <  1.000e-06    |      4.731e-07 c16_wz_vh_th : 0
  calypso_7b2b_1 CBD:       tsetup  <  1.000e-06    |      4.438e-07 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:         ugbw  >  1.000e+07    | o    6.222e+06 c6_ws_vl_th : 0.378
  calypso_7b2b_1 CBD:      vds_drv  >  0.000e+00    |      6.171e-02 c5_ws_vl_tl : 0
  calypso_7b2b_1 CBD:      vgs_drv  >  0.000e+00    |      5.395e-02 c1_wp_vl_tl : 0

The initial sets of corners where the performance measures will be evaluated 
are constructed

.. code-block:: none

  calypso_7b2b_1 CBD: Pass 1, updating corner lists
  calypso_7b2b_1 CBD:   area: ['nom']
  calypso_7b2b_1 CBD:   cmrr: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   dep gain: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   dep gain_com: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   isup: ['c3_wp_vh_tl']
  calypso_7b2b_1 CBD:   overshdn: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   overshup: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   pm: ['c3_wp_vh_tl']
  calypso_7b2b_1 CBD:   psrr_vdd: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   dep gain: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   dep gain_vdd: ['c10_wo_vl_th']
  calypso_7b2b_1 CBD:   psrr_vss: ['c5_ws_vl_tl']
  calypso_7b2b_1 CBD:   dep gain: ['c10_wo_vl_th', 'c5_ws_vl_tl']
  calypso_7b2b_1 CBD:   dep gain_vss: ['c5_ws_vl_tl']
  calypso_7b2b_1 CBD:   slewdn: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   slewup: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   swing: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   tsetdn: ['c16_wz_vh_th']
  calypso_7b2b_1 CBD:   tsetup: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   ugbw: ['c6_ws_vl_th']
  calypso_7b2b_1 CBD:   vds_drv: ['c5_ws_vl_tl']
  calypso_7b2b_1 CBD:   vgs_drv: ['c1_wp_vl_tl']

an the optimization is started. The optimizer stops when it finds a circuit 
that satisfies all design requirements across the intial corner sets. Next, 
this circuit is evaluated across all corners. 

.. code-block:: none

  calypso_7b2b_1 CBD: Pass 2, full corner evaluation
  calypso_7b2b_1 CBD: Pass 2, corner summary
  calypso_7b2b_1 CBD:         area  <  9.000e-09    |      1.024e-09    nom : 0
  calypso_7b2b_1 CBD:         cmrr  >  9.000e+01    | o    7.958e+01 c13_wz_vl_tl : 0.116
  calypso_7b2b_1 CBD:         gain  >  6.000e+01    |      6.935e+01 c1_wp_vl_tl : 0
  calypso_7b2b_1 CBD:         isup  <  1.000e-03    |      1.991e-04 c11_wo_vh_tl : 0
  calypso_7b2b_1 CBD:     overshdn  <  1.000e-01    |      9.678e-03 c9_wo_vl_tl : 0
  calypso_7b2b_1 CBD:     overshup  <  1.000e-01    |      9.448e-02 c9_wo_vl_tl : 0
  calypso_7b2b_1 CBD:           pm  >  5.000e+01    |      6.155e+01 c9_wo_vl_tl : 0
  calypso_7b2b_1 CBD:     psrr_vdd  >  6.000e+01    |      7.090e+01 c14_wz_vl_th : 0
  calypso_7b2b_1 CBD:     psrr_vss  >  6.000e+01    |      8.204e+01 c16_wz_vh_th : 0
  calypso_7b2b_1 CBD:       slewdn  >  2.000e+06    |      1.035e+07 c14_wz_vl_th : 0
  calypso_7b2b_1 CBD:       slewup  >  2.000e+06    |      9.645e+06 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:        swing  >  1.000e+00    |      1.320e+00 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:       tsetdn  <  1.000e-06    |      1.219e-07 c16_wz_vh_th : 0
  calypso_7b2b_1 CBD:       tsetup  <  1.000e-06    |      2.013e-07 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:         ugbw  >  1.000e+07    |      1.561e+07 c6_ws_vl_th : 0
  calypso_7b2b_1 CBD:      vds_drv  >  0.000e+00    |      5.821e-02 c5_ws_vl_tl : 0
  calypso_7b2b_1 CBD:      vgs_drv  >  0.000e+00    |      5.708e-02 c13_wz_vl_tl : 0

Corners where some design requirement is not satisfied are added to 
the corresponding corner sets 

.. code-block:: none

  calypso_7b2b_1 CBD: Pass 2, updating corner lists
  calypso_7b2b_1 CBD:   cmrr: ['c10_wo_vl_th', 'c13_wz_vl_tl']
  calypso_7b2b_1 CBD:   dep gain: ['c10_wo_vl_th', 'c5_ws_vl_tl', 'c13_wz_vl_tl']
  calypso_7b2b_1 CBD:   dep gain_com: ['c10_wo_vl_th', 'c13_wz_vl_tl']

and a new optimization is started. This procedure is repeated until a circuit 
is found that satisfies all design requirements across all corners. In the 
end the values of the design parameters obtained by the optimizer are printed 

.. code-block:: none

          c_out:    1.110200e-12
         diff_l:    3.247602e-06
         diff_w:    6.042974e-06
         load_l:    1.614003e-06
         load_w:    5.796995e-05
         mirr_l:    7.731257e-07
        mirr_ld:    3.243680e-06
         mirr_w:    9.007543e-05
        mirr_wd:    1.878471e-05
        mirr_wo:    8.233483e-05
          out_l:    4.108898e-07
          out_w:    6.003844e-05
          r_out:    3.574993e+04

followed by the circuit's performance. 

.. code-block:: none

        area  <  9.000e-09    |      1.010e-09    nom : 0
        cmrr  >  9.000e+01    |      9.040e+01 c10_wo_vl_th : 0
        gain  >  6.000e+01    |      6.972e+01 c1_wp_vl_tl : 0
        isup  <  1.000e-03    |      2.096e-04 c11_wo_vh_tl : 0
    overshdn  <  1.000e-01    |      1.884e-03 c9_wo_vl_tl : 0
    overshup  <  1.000e-01    |      5.750e-02 c9_wo_vl_tl : 0
          pm  >  5.000e+01    |      5.721e+01 c9_wo_vl_tl : 0
    psrr_vdd  >  6.000e+01    |      7.226e+01 c1_wp_vl_tl : 0
    psrr_vss  >  6.000e+01    |      8.058e+01 c4_wp_vh_th : 0
      slewdn  >  2.000e+06    |      6.449e+06 c6_ws_vl_th : 0
      slewup  >  2.000e+06    |      6.259e+06 c6_ws_vl_th : 0
       swing  >  1.000e+00    |      1.332e+00 c6_ws_vl_th : 0
      tsetdn  <  1.000e-06    |      1.846e-07 c16_wz_vh_th : 0
      tsetup  <  1.000e-06    |      1.956e-07 c5_ws_vl_tl : 0
        ugbw  >  1.000e+07    |      1.435e+07 c6_ws_vl_th : 0
     vds_drv  >  0.000e+00    |      8.508e-02 c5_ws_vl_tl : 0
     vgs_drv  >  0.000e+00    |      2.965e-02 c1_wp_vl_tl : 0

We can see that the corners where performances reach their worst 
value come from the set of 17 initially defined corners. 
Because all design requirements are satisfied all penalty 
contributions are 0. 

Note that due to the random nature of the delays on the network 
parallel runs may yield different solutions for the same design 
problem.

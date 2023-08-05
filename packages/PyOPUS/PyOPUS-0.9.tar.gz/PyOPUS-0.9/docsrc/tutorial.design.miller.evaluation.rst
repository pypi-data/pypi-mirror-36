.. _design-miller-evaluation:
	
Evaluation of opamp's performance
=================================

We are going to set up the evaluation of a Miller opamp. For now we are not 
going to use any of the :mod:`pyopus.design` module's facilities. The script 
from file `01-evaluator.py <../../../demo/design/miller/01-evaluator.py>`_ 
in folder `demo/design/miller/ <../../../demo/design/miller/>`_

.. literalinclude:: ../demo/design/miller/01-evaluator.py
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

Finally, a :class:`pyopus.evaluator.performance.PerformanceEvaluator` 
object is created from ``heads``, ``analyses``, ``measures``, and 
``variables`` defined in 
`definitions.py <../../../demo/design/miller/definitions.py>`_ 
and the ``corners`` variable constructed in this script. The evaluator 
will store the waveforms produced by the simulator in the local temporary 
folder of the machine where the results were computed by a simulator. 
The performance evaluator is then called (``pe()``) and the values of the 
initial design parameters and nominal statistical parameters are passed. 
These parameters are added to the input netlist for the simulator. 

When the evaluation is finished the performance measures are printed

.. code-block:: none

      area |             nom:    1.179e-09
      cmrr |             nom:    5.796e+01
      gain |             nom:    6.624e+01
  gain_com |             nom:    8.277e+00
  gain_vdd |             nom:   -2.624e+01
  gain_vss |             nom:    3.777e+00
   in1kmn2 |             nom:    1.581e-16
 in1kmn2id |             nom:    1.581e-16
 in1kmn2rd |             nom:    0.000e+00
  inoise1k |             nom:    3.344e-14
      isup |             nom:    3.010e-04
  onoise1k |             nom:    3.337e-14
    out_op |             nom:    6.979e-03
  overshdn |             nom:    7.176e-02
  overshup |             nom:    8.924e-02
        pm |             nom:    7.004e+01
  psrr_vdd |             nom:    9.247e+01
  psrr_vss |             nom:    6.246e+01
    slewdn |             nom:    1.082e+07
    slewup |             nom:    1.006e+07
     swing |             nom:    1.474e+00
    tsetdn |             nom:    1.925e-07
    tsetup |             nom:    2.094e-07
      ugbw |             nom:    6.641e+06
   vds_drv |             nom: [0.58454814 0.8205568  0.433882   0.11164392 0.82752772 0.55567868 0.32221448 0.80099198]
   vgs_drv |             nom: [0.2121875  0.20869958 0.02675759 0.02674103 0.02677772 0.39175785 0.39175785 0.10682108]
   
Next, the list of stored waveform files and hosts where they are stored is 
printed
	
.. code-block:: none

  Result files across hosts
  {(None, ('nom', 'ac')): '/tmp/restemp_calypso_6370_2_CnomAac_ssv1t8be',
   (None, ('nom', 'accom')): '/tmp/restemp_calypso_6370_4_CnomAaccom_8m074mfy',
   (None, ('nom', 'acvdd')): '/tmp/restemp_calypso_6370_6_CnomAacvdd_p6xcmn4x',
   (None, ('nom', 'acvss')): '/tmp/restemp_calypso_6370_3_CnomAacvss_krfc4fxj',
   (None, ('nom', 'dc')): '/tmp/restemp_calypso_6370_2_CnomAdc_n8vka_51',
   (None, ('nom', 'noise')): '/tmp/restemp_calypso_6370_2_CnomAnoise_yqk65tgi',
   (None, ('nom', 'op')): '/tmp/restemp_calypso_6370_2_CnomAop_m4w5zmfv',
   (None, ('nom', 'tran')): '/tmp/restemp_calypso_6370_2_CnomAtran_ujakw14_',
   (None, ('nom', 'translew')): '/tmp/restemp_calypso_6370_5_CnomAtranslew_0t0d6u74',
   (None, ('nom', None)): '/tmp/restemp_calypso_6370_1Cnom_4l03mlni'}

A call to :meth:`pyopus.evaluator.performance.PerformanceEvaluator.collectResultFiles` 
is made. This moves the result files from temporary storage on respective hosts to the 
current folder of the host that invoked the evaluator. The list of collected 
files is printed
	
.. code-block:: none

  Collected result files
  {('nom', None): 'res_nom.pck',
   ('nom', 'ac'): 'res_nom_ac.pck',
   ('nom', 'accom'): 'res_nom_accom.pck',
   ('nom', 'acvdd'): 'res_nom_acvdd.pck',
   ('nom', 'acvss'): 'res_nom_acvss.pck',
   ('nom', 'dc'): 'res_nom_dc.pck',
   ('nom', 'noise'): 'res_nom_noise.pck',
   ('nom', 'op'): 'res_nom_op.pck',
   ('nom', 'tran'): 'res_nom_tran.pck',
   ('nom', 'translew'): 'res_nom_translew.pck'}	

The file holding the environment in which the performance measures without 
an analysis were evaluated is loaded and the environment is printed

.. code-block:: none

  {'isNmos': [1, 1, 1, 1, 1, 0, 0, 0],
   'm': <module 'pyopus.evaluator.measure' from '/home/arpadb/pytest/pyopus/evaluator/measure.py'>,
   'mosList': ['xmn1', 'xmn2', 'xmn3', 'xmn4', 'xmn5', 'xmp1', 'xmp2', 'xmp3'],
   'np': <module 'numpy' from '/usr/local/lib/python3.5/dist-packages/numpy/__init__.py'>,
   'param': {'c_out': 8.21e-12,
             'diff_l': 1.08e-06,
             'diff_w': 7.73e-06,
             'gu0nmm': 0.0,
             'gu0pmm': 0.0,
             'gvtnmm': 0.0,
             'gvtpmm': 0.0,
             'load_l': 2.57e-06,
             'load_w': 3.49e-05,
             'mirr_l': 5.63e-07,
             'mirr_ld': 5.63e-07,
             'mirr_w': 7.46e-05,
             'mirr_wd': 7.46e-05,
             'mirr_wo': 7.46e-05,
             'mn1u0': 0.0,
             'mn1vt': 0.0,
             'mn2u0': 0.0,
             'mn2vt': 0.0,
             'mn3u0': 0.0,
             'mn3vt': 0.0,
             'mn4u0': 0.0,
             'mn4vt': 0.0,
             'mn5u0': 0.0,
             'mn5vt': 0.0,
             'mp1u0': 0.0,
             'mp1vt': 0.0,
             'mp2u0': 0.0,
             'mp2vt': 0.0,
             'mp3u0': 0.0,
             'mp3vt': 0.0,
             'out_l': 3.75e-07,
             'out_w': 4.8e-05,
             'r_out': 19.7,
             'temperature': 25,
             'vdd': 1.8},
   'result': {'gain': {'nom': 66.23930624546703},
              'gain_com': {'nom': 8.276939732033867},
              'gain_vdd': {'nom': -26.235135394608754},
              'gain_vss': {'nom': 3.776680236411179},
              'in1kmn2': {'nom': 1.5814509234426615e-16},
              'in1kmn2id': {'nom': 1.5814509234426615e-16},
              'in1kmn2rd': {'nom': 0.0},
              'inoise1k': {'nom': 3.343611881913326e-14},
              'isup': {'nom': 0.0003009768725548291},
              'onoise1k': {'nom': 3.3371005496346185e-14},
              'out_op': {'nom': 0.006979234805394086},
              'overshdn': {'nom': 0.07176477049919334},
              'overshup': {'nom': 0.08923807202380866},
              'pm': {'nom': 70.04068497059643},
              'slewdn': {'nom': 10818342.824614132},
              'slewup': {'nom': 10059147.304855734},
              'swing': {'nom': 1.4744709441983554},
              'tsetdn': {'nom': 1.9248788635101697e-07},
              'tsetup': {'nom': 2.0939194104629665e-07},
              'ugbw': {'nom': 6641243.731566119},
              'vds_drv': {'nom': array([0.58454814, 0.8205568 , 0.433882  , 0.11164392, 0.82752772, 0.55567868, 0.32221448, 0.80099198])},
              'vgs_drv': {'nom': array([0.2121875 , 0.20869958, 0.02675759, 0.02674103, 0.02677772, 0.39175785, 0.39175785, 0.10682108])}}}
	    
.. figure:: design-miller-init-nom-gain.png
	:scale: 80%
	
	Gain of the initial Miller amplifier in nominal corner.

Next, the file holding the waveforms produced by the ``ac`` analysis is 
loaded. The frequency scale and the gain in dB are extracted and plotted. 

The script cleans up all temporary files. Only the collected result files 
(.pck) remain on disk. 

If we start the script on multiple local CPUs with

.. code-block:: none

  mpirun -n 5 python3 01-evaluator.py
  
we can see that the evaluation runs faster because analyses are distributed
across multiple CPUs. The part of the output that lists the remotely stored 
result files changes to

.. code-block:: none

  Result files across hosts
  {(MPIHostID('calypso'), ('nom', 'ac')): '/tmp/restemp_calypso_65c2_1_CnomAac_xhh3ropu',
   (MPIHostID('calypso'), ('nom', 'accom')): '/tmp/restemp_calypso_65c4_1_CnomAaccom_utgk23ks',
   (MPIHostID('calypso'), ('nom', 'acvdd')): '/tmp/restemp_calypso_65c3_1_CnomAacvdd_j7r4vd4p',
   (MPIHostID('calypso'), ('nom', 'acvss')): '/tmp/restemp_calypso_65c3_1_CnomAacvss_7wgcjv2e',
   (None, ('nom', None)): '/tmp/restemp_calypso_65c1_1Cnom_2zohpbz8',
   (MPIHostID('calypso'), ('nom', 'dc')): '/tmp/restemp_calypso_65c2_1_CnomAdc_zhrfjulg',
   (MPIHostID('calypso'), ('nom', 'noise')): '/tmp/restemp_calypso_65c2_1_CnomAnoise_b4p6y1u5',
   (MPIHostID('calypso'), ('nom', 'op')): '/tmp/restemp_calypso_65c2_1_CnomAop_v3a179se',
   (MPIHostID('calypso'), ('nom', 'tran')): '/tmp/restemp_calypso_65c2_1_CnomAtran_7zynujcs',
   (MPIHostID('calypso'), ('nom', 'translew')): '/tmp/restemp_calypso_65c5_1_CnomAtranslew_fh19g7hp'}
  
We can see that only the ('nom', None) corner-analysis pair is stored locally 
because the corresponding performance measures were evaluated on the local machine 
(the one that invoked the evaluator). 


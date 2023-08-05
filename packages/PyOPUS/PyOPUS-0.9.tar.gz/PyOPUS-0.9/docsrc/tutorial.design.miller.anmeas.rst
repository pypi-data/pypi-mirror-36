.. _design-miller-anmeas:

A closer look at analyses and performance measures
==================================================

In this section we are going to take a closer look at analyses and performance 
measures we defined in the copmmon part of the problem definition. 

Analysis ``op`` is an operating point analysis. No special arguments are 
specified in the command string (``op()``) because this analysis has none. 
The amplifier definition ``def`` and the top-level circuit ``tb`` are 
included in the simulator's input netlist. Four performance measures are 
extracted from operating point analysis results: 
	
  * ``isup`` is the current supplied by the power supply. It is extracted 
    with a simple scipt ``isup=-i('vdd')``. 
  * ``out_op`` is the output voltage operating point. The extraction 
    is pefromed by an expression ``v('out')``. One could also write a 
    script (``out_op=v('out')``) or a script (``__result=v('out')``). 
  * ``vgs_drv`` is the Vgs overdrive voltage (i.e. how much above the 
    threshold is the operating point Vgs voltage of a transistor. The 
    result of this measurement is a vector with as many entries as there 
    are transistors defined in variable ``mosList``. The script is written 
    with comments and is self-explanatory. 
  * ``vds_drv`` is the Vds overdrive voltage (i.e. how much above the 
    boundary of the saturation is the operating point Vds voltage). The 
    script is similar to the ``vgs_drv`` script. 

The ``dc`` analysis sweeps the input voltage source Vin1 from -2V to 2V 
with 100 uniform (linearly spaced) steps. The amplifier definition ``def`` 
and the top-level circuit ``tb`` are included in the simulator's input 
netlist. The circuit has a feedback loop comprising R1 and R2. Due to this 
feedback the operating point (where Vin1 is 0V) is in the middle of the 
amplifier's active region. Sweeping Vin1 from -2V to 2V results in the 
output going from positive saturation across the active region into the 
negative saturation. If we observe the output voltage against the input
voltage between the amplifier's non-inverting (``inp``) and inverting input 
(``inn``) we get the amplifier' DC characteristic for differential gain. 
By computing the derivative of y wrt. x in this graph we get the dependence 
of the gain on the input differential voltage. This dependence is a 
bell shaped curve. One desires the bell to be as wide as possible. We express 
the width of the curve with the ``swing`` perfromance measure which 
computes the equivalent output voltage range width where the gain is above 
50% of the maximal gain. 

The ``ac`` analysis sweeps the frequency from 1Hz to 1Thz logarithmically 
with 10 points per decade. The analysis includes the amplifier definition ``def`` 
and the top-level circuit ``tb`` in the simulator's input netlist. 
The AC excitation comes from the Vin1 input voltage source whose ac parameter 
is set to 1. 

Its results are used for computing 

  * differential gain (``gain``) which is obtained as the magnitude of 
    the ratio between output and input differential voltage obtained with 
    expression ``m.ACmag(m.ACtf(v('out'), v('inp', 'inn')))``. Because the 
    expression results in a vector holding the values of gain for all 
    simulated frequency points we extract the first component which 
    corresponds to gain at 1Hz. 
  * unit-gain bandwidth (``ugbw``) which is the frequency where the 
    differential gain becomes 1. It is computed with expression 
    ``m.ACugbw(m.ACtf(v('out'), v('inp', 'inn')), scale())``. The 
    expression uses the frequency scale to compute the value of ``ugbw``. 
  * Phase margin (``pm``) is the difference in phase between -180 degrees 
    and the phase at unity-gain. It is computed with expression 
    ``m.ACphaseMargin(m.ACtf(v('out'), v('inp', 'inn')))``. 

Three additional ac analyses (``accom``, ``acvdd``, and ``acvss``) are 
produce the waveforms from which the gains from Vdd1, Vss1, and Vcom to 
the circuit's output. All of them use the ``tbrr`` top level circuit 
instead of ``tb``. They differ only in the AC excitation which is selected 
by three netlist parameters: ``accom``, ``acvdd``, and ``acvss``. Their 
frequency scales are indetical to that of the ``ac`` analysis so that 
the frequency response of the CMRR, PSSR_VDD, and PSRR_VSS can be computed 
by dividing the respective gain vectors. The following performance measures 
are computed

  * From ``accom`` analysis ``gain_com`` (common mode gain at 1Hz) which is 
    obtained as ``m.ACmag(m.ACtf(v('out'), 1.0))[0]``. Note that the input 
    signal is equal to 1 (due to the ``ac`` parameter of the Vcom voltage 
    source (which is set by the ``accom`` netlist parameter. 
  * From ``acvdd`` analysis ``gain_vdd`` (gain from Vdd to output at 1Hz). 
  * From ``acvss`` analysis ``gain_vss`` (gain from Vdd to output at 1Hz). 

Noise analysis names ``noise`` sweeps the frequency across the same scale 
as the ``ac`` analysis. It uses the ``tb`` top level circuit. and computes 
the output noise at the amplifier's output and the equivalent input noise 
at Vin1. The following performance measures are computed from its results:
	
  * Output noise power spectrum density at 1kHz ``onoise1k`` which is 
    computed with expression 
    ``m.XatI(ns('output'), m.IatXval(scale(), 1e3)[0])``
    The function ``m.IatXval`` finds the position in the frequency scale 
    that corresponds to 1kHz. The obtained position is used for extracting 
    the noise spectral density from the output noise spectrum. 
  * Equivalent input noise power spectrum density at 1kHz ``inoise1k`` which 
    is computed with expression 
    ``m.XatI(ns('input'), m.IatXval(scale(), 1e3)[0])``
    The function ``m.IatXval`` finds the position in the frequency scale 
    that corresponds to 1kHz. The obtained position is used for extracting 
    the noise spectral density from the equivalent input noise spectrum. 
  * The contribution of Mn2's channel noise to the equivalent input power 
    spectrum density at 1kHz (``in1kmn2id``) computed as 
    ``m.XatI(ns('input', ipath('xmn2', 'x1', 'm0'), 'id'), m.IatXval(scale(), 1e3)[0])``
    The ipath function is used for constructing the fully qualified instance 
    name of the built-in MOS instance corresponding to Mn2.
  * The contribution of Mn2's drain resistance thermal noise to the 
    equivalent input power spectrum density at 1kHz (``in1kmn2rd``) computed as 
    ``m.XatI(ns('input', ipath('xmn2', 'x1', 'm0'), 'id'), m.IatXval(scale(), 1e3)[0])``
  * The total contribution of Mn2's noise to the equivalent input power 
    spectrum density at 1kHz. (``in1kmn2``) computed as 
    ``m.XatI(ns('input', ipath('xmn2', 'x1', 'm0')), m.IatXval(scale(), 1e3)[0])``

Transient analysis ``tran`` uses the ``tb`` top level circuit and computes 
the response to a pulse generated by Vin1. The pulse initial level (lev1), 
pulse level (lev2), start time (tstart), rise time (tr), fall time (tf), and 
width (pw) are specified in the ``heads`` variable (see previous section). 
The pulse rises from lev1 to lev2 and then drops down back to lev1. Because 
the top level circuit is an inverting amplifier the amplifier's output first 
falls and then rises again. The following performance measures are computed 
from the resulting waveforms. 

  * undershoot at falling edge of the amplifier's output (``overshdn``). 
    Expression
    ``m.Tundershoot(v('out'), scale(), t1=param['tstart'], t2=(param['pw']+param['tstart']+param['tr']))`` 
    is used. Arguments ``t1`` and ``t2`` specify the time window within which 
    the undershoot happens (between t=tstart and t=tstart+tr+pw). The reference 
    signal levels are taken at both ends of the specified time window. 
  * oveshoot at rising edge of the amplifier's output (``overshup``). 
    The ``m.Tovershoot`` function is used in the expression on time window 
    between t=tstart+tr+pw and the end of the waveform. 
  * settling time at the falling edge of amplifier's output (``tsetdn``) 
    computed with expression
    ``m.TsettlingTime(v('out'), scale(), t1=param['tstart'], t2=(param['pw']+param['tstart']+param['tr']))``
  * settling time at the rising edge of amplifier's output (``tsetup``) 
  
Transient analysis ``translew`` also uses the ``tb`` top level circuit. It 
is identical to ``tran`` analysis with one exception. The initial level and 
the pulse level are chosen in such manner that the amplifier's output reaches 
saturation level. Two performance measures are obtained from the resulting 
waveforms

  * The falling slew rate ``slewdn`` is observed within the time window between 
    t=tstart and t=tstart+tr+pw. It is compunted with expression 
    ``m.TslewRate('falling', v('out'), scale(), t1=param['tstart'], t2=(param['pw']+param['tstart']+param['tr']))``
  * The rising slew rate ``slewup`` is observed within the time window between 
    t=tstart+tr+pw and waveform end. The expression is similar to the one used 
    for computing ``slewdn``. 

Certain performance measures are not computed from analysis results. Their 
value depends on previously evaluated performance measures, netlist parameters, 
and user-defined variables. A netlist parameter named ``diff_w`` can be accessed 
as ``param['diff_w']``. Variables are accessed by their names. The results of 
performance measures that were computed from analysis results are accessed 
as ``result[measure_name][corner_name]``. The variable ``cornerName`` holds the 
name of the corner for which the performance measure is being evaluated. 

  * ``area`` is the approximate circuit area. It is computed from netlist 
    parameters that specify device dimensions.
  * ``cmrr`` is the common mode rejection ratio computed from ``gain`` and 
    ``gain_com``. Because both gains are in decibels, CMRR is computed with 
    a simple subtraction.
    ``result['gain'][cornerName]-result['gain_com'][cornerName]``
  * ``psrr_vdd`` is the power supply rejection ratio of the Vdd power supply. 
  * ``psrr_vss`` is the power supply rejection ratio of the Vss power supply. 

.. _design-miller-problem:

Common part of the design problem definition
============================================

The part of the problem definition that is common to all design algorithms 
is defined in file `definitions.py <../../../demo/design/miller/definitions.py>`_ 
in folder `demo/design/miller/ <../../../demo/design/miller/>`_

.. literalinclude:: ../demo/design/miller/definitions.py
   :language: python
   
Variable ``heads`` contains the definitions of all simulators that are going 
to be used. It is a dictionary. We are going to use Spice Opus only. Therefore 
the dictionary has only one entry named ``opus`` which is also a dictionary, 
The first two members (``simulator`` and ``settings``) specify the simulator 
and the arguments passed to the simulator wrapper at initialization (e.g. 
debug level). 

Dictionary ``moddefs`` lists the netlist modules that will be 
used for constructing the input netlist for the simulator. Modules ``def``, 
``tb`` and ``tbrr`` correspond to the amplifier definition (``miller.inc``), 
the first top level circuit (``topdc.inc``), and the second top level circuit 
(``toprr.inc``). The remaining modules correspond to various MOS models in 
the foundry's library: ``tm`` for the typical model, ``wp`` for the worst power 
model, ``ws`` for worst speed model, ``wo`` for worst one model, ``wz`` for 
worst zero model, and ``mc`` for the Monte Carlo model used in Monte Carlo 
analysis and mismatch analysis. 

Dictionary ``options`` lists the simulator options passed via the netlist 
(in case of Spice Opus they are passed with the ``.options`` directive). 

Dictionary ``params`` specifies the netlist parameters that will be defined 
with ``.param`` statements. We can see that the bias current, the input 
pulse source shape, and the output load are specified here. 

Variable ``variables`` is a dictionary specifying the variables that will 
be available during mesure evaluations and in the specifications of quantities 
that need to be saved. In our case we define the list of MOS instances in 
the circuit (``mosList``) and corresponding flags that specify if a transistor 
is a NMOS or a PMOS device (``isNmos``). The latter is used only in the 
Spectre demo because Spectre handles Vgs and Vds for PMOS transistors with 
a negative sign in constrast to NMOS transistors where the sign is positive. 

The ``analyses`` variable lists the analyses pefromed by simulators. 
For every analysis one has to specify the simulator to use (``head`` name): 
the list of netlist modules that will be included in the simulator's input 
netlist (``modules``), simulator options (``options``), netlist parameters 
(``params``), the list of non-default quantities for the simulator to save 
in its output files (``saves``), and the actual analysis that the simulator 
should invoke (``analysis``). The simulator options and netlist parameters 
specified here override those specified in the ``heads`` variable. 

The ``saves`` entry does not have to be specified. If it is omitted the 
default quantities are saved. An example of a custom save quantity list can 
be seen in the definitions of the ``op`` analysis. Here the default quantities 
are saved (``all()``) and certain properties of MOS transistors (``vgs``, 
``vth``, ``vds``, and ``vdsat``) are saved for all MOS transistors defined in 
variable ``mosList``. The ``ipath`` function is used to add the outer path 
(``x1``) and the inner path (``mo``) to form a fully qualified instance name 
of the built-in MOS device corresponding to an individual transistor because 
only built-in devices have special quantities that can be stored. 

The ``measures`` variable is a dictionary defining the performance measures 
that will be extracted from simulator results. For every measure we must 
specify the analysis name (``analysis``), the expression or a script for 
computing it (``expression``), and a flag if the measure produces a vector 
(``vector``). The latter can be omitetd if the measure produces a scalar. 
Optionally one can also specify the lower and/or upper bound on acceptable 
performance (``lower`` and ``upper``). If the measure produces a vector 
this bound is applied to all components of a vector. 

Some measures are not computed directly from simulation results. Instead 
they are computed from other measures. For such measures ``None`` is specified 
as analysis name. If such a measure is computed from other measures a list 
of measure names on which the measure depends must be given (``depends``). 

The ``designParams`` variable lists the design parameters. For every parameter 
the lower (``lo``) and the upper (``hi``) bound are specified, as well as 
the initial value (``init``). 

The ``statParams`` variable lists the statistical parameters. For every 
statistical parameter the lower and the upper bound is specified (``lo`` and 
``hi``). All statistical parameters are for now assumed to be independent 
normally distributed random variables with mean 0 and variance 1. 

The ``opParams`` variable lists the operating parameters of a circuit. In 
our case these are the supply voltage (``vdd``) and the temperature. For every 
parameter one has to specify its lower and upper bound (``lo`` and ``hi``), 
as well as, its nominal value (``init``) are specified. One could also 
simulate this circuit without taking into account that the operating 
temperature can change over a range of values. In such cases the temperature 
should be specified in the ``heads`` variable under ``params``. 

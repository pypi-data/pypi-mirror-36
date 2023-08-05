Simulator setup
===============

PyOPUS is capable of evaluating a circuit with multiple simulators. Of course, 
you must provide input files for all simulators. We are going to use only 
one simulator - Spice Opus. We start by adding a new simulator setup. 
Right-click the "Simulator setups" entry in the project tree and select 
"Add item after". 

A new simulator setup will be created. Simulator setup names must be unique 
identifiers. Type the name of the setup ("opus") and select it. 
Its properties are available in the right-half of the Project tab. 

.. figure:: gui-project-simulator.png
	:scale: 75%
	
	Editing a simulator setup in the GUI. 

Select "Spice Opus" as the simulator type. Under SImulator settings you can 
enter the arguments that will be passed to the simulator class at construction 
of a simulator object. Under Simulator options you can specify the options 
passed to the simulator via its input netlist. These options are valid for all 
analyses. Under Parameters you can enter the values of netlist parameters 
that are common to all analyses and all corners. Finally, under Input modules 
you define netlist modules that will be used by analyses and corners. 

We define several input modules for our example. 

   * ``def`` is the definition of the opamp in file ``miller.inc``
   * ``tb`` is the top-level test circuit in file ``topdc.inc``. 
     It is used for the OP, DC, AC, TRAN, and NOISE analysis. 
   * ``tbrr`` is the top-level test circuit in file ``toprr.inc``. 
     It is used for the AC analyses that compute the common mode gain 
     and the gain from both power supplies to the circuit's output.
   * ``tm`` is the ``tm`` section in MOS model library file ``cmos180n.lib`` 
     where the typical MOS transistor models are defined.
   * ``wp`` is the ``wp`` section in MOS model library file ``cmos180n.lib`` 
     where the worst-power MOS transistor models are defined.
   * ``ws`` is the ``ws`` section in MOS model library file ``cmos180n.lib`` 
     where the worst-speed MOS transistor models are defined.
   * ``wo`` is the ``wo`` section in MOS model library file ``cmos180n.lib`` 
     where the worst-one MOS transistor models are defined. 
   * ``wz`` is the ``wz`` section in MOS model library file ``cmos180n.lib`` 
     where the worst-zero MOS transistor models are defined. 
   * ``mc`` is the ``mc`` section in MOS model library file ``cmos180n.lib`` 
     where the Monte Carlo MOS transistor models for statistical analysis 
     are defined. 

.. figure:: gui-project-simulator-modules.png
	:scale: 75%
	
	Setting up input modules in simulator setup. 
	
Note that you can use the hash notation for simulator settings, simulator 
options, and netlist parameters. Input module names must be unique identifiers. 
Input module names, parameter names, and simulator option names must be unique 
identtifiers. 

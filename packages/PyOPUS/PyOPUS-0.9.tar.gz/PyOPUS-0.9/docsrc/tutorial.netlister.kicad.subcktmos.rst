.. _mosmm.inc : ../../../demo/kicad/04-subcktmodel/mosmm.inc

.. _kicad-pyopus-subcktmodel:

Customization example: netlisting MOS devices as subcircuits
============================================================
In section :ref:`kicad-pyopus-library` the MOS transistors were simulated as builtin 
SPICE devices (i.e. their names all started with M to indicate this). What to do 
when your MOS transistors models define them as subcircuits. This is often the case 
in integrated circuit design where several other parameters that define the parasitics 
must be specified (like AD, AS, PD, AS, ...). These parameters generally depend on 
channel dimensions. Therefore MOS transistor models are often defined as subcircuits 
that automatically compute these parameters from channel dimensions. For our example 
suppose we have two such subcircuits defined, one for NMOS and one for PMOS. The 
definition of these two subcircuits can be found in file mosmm.inc_. 

.. literalinclude:: ../demo/kicad/04-subcktmodel/mosmm.inc
   :language: none

The file defines two subcircuits named ``nmosmod`` and ``pmosmod`` that wrap the two 
builtin MOS models which are also names ``nmosmod`` and ``pmosmod``. Both of them have 
5 parameters (W, L, M, VTMM and U0MM). The meaning of VTMM and U0MM will be explained 
in section :ref:`kicad-pyopus-mmpar`. For now we assume they are set to their default 
value 0. 

To use these two subcircuits we would have to add several Fields to every MOS instance 
in the Miller OTA schematic. But we can get away with much less work if we alter the 
netlister behavior with the following 
`netlister.json <../../../demo/kicad/04-subcktmodel/netlister.json>`_ file. 

.. literalinclude:: ../demo/kicad/04-subcktmodel/netlister.json
   :language: none

This netlists the MOS transistors as subcircuits. The name prefix is now ``X`` instead 
of ``M``. The list of parameters includes parameters of the above defined subcircuits 
instead of those available for builtin MOS devices. Most importantly, the netlisting 
pattern is changed to that of a subcircuit. 

If we netlist the ``miller.sch`` schematic again we get the following netlist. 

.. literalinclude:: ../demo/kicad/04-subcktmodel/miller.inc
   :language: none

For the simulation we must include the two subcircuit definitions from mosmm.inc_. 
We do that in the top level schematic ``topdc.sch``. 

.. figure:: kicad-subcktmodel-topdc.png
	:scale: 60%
	
	Top level circuit definition that included the ``mosmm.inc`` file. 

Demo files for this section can be found `here <../../../demo/kicad/04-subcktmodel>`_.

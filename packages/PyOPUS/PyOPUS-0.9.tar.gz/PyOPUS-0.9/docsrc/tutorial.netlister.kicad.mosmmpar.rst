.. _mosmm.inc : ../../../demo/kicad/05-mosmmpar/mosmm.inc

.. _kicad-pyopus-mmpar:

Customization example: generating MOS mismatch parameters
=========================================================

In Section :ref:`kicad-pyopus-subcktmodel` we customized the netlister behavior so 
that instead of generating builtin MOS devices it produced a netlist where MOS 
transistors were subcircuits defined in file mosmm.inc_. Manufacturing introduces 
variation in the MOS transistor properties. Therefore two identically designed MOS 
transistors do not share the same characteristics. This effect is called mismatch 
and is modelled with additional parameters VTMM and U0MM. Random process variations 
are transformed to these two parameters in such manner that if one treats VTMM and 
U0MM as two independent normally distributed random variables with zero mean and 
standard deviation 1 the correct joint probability distribution of MOS model 
parameters are reproduced. 

In simulations parameters VTMM and U0MM are used by various analyses. To make them 
accessible their values are taken from global parameters. This means that two 
fields must be added to every MOS transistor in the ``miller.sch`` schematic. 
It is more simple to change the netlisting rules for MOS transistors with the 
following `netlister.json <../../../demo/kicad/05-genmmpar/netlister.json>`_ file. 

.. literalinclude:: ../demo/kicad/05-genmmpar/netlister.json
   :language: none

For a transistor named ``m1`` in the schematic ``#REFORIG()vt`` expands to 
``m1vt``. This way the ``vtmm`` parameter of ``m1`` can be set via the ``m1vt`` 
global circuit parameter. To avoid neltlisting VTMM and U0MM values that are 
specified as component fields these two parameters are not included in the 
``Parameters`` member of the device mapping. 

By netlisting the ``miller.sch`` schematic we get the following netlist. 

.. literalinclude:: ../demo/kicad/05-genmmpar/miller.inc
   :language: none

For the simulation all the generated global circuit parameters must be defined. 
We do that in the top level schematic ``topdc.cir``. There are two ways how to 
add parameter values to a schematic. 

The first if to use the PARAM component from the KiCad pyopus library. One PARAM 
component must be added for every global parameter we must define. This makes the 
schematic portable so that when support for other simulators will be added these 
parameter definition will be netlisted correctly. 

The second one is less portable but also involes less clicking. We add a text 
block to the toplevel schematic with the `.param`` statements that define the 
required global parameters. The disadvantage of this approach is that it is 
simulator specific. Due to the simulator syntax it sould be fine for Spice Opus 
and HSPICE, but not for Spectre. 

.. figure:: kicad-genmmpar-topdc.png
	:scale: 60%
	
	Top level circuit definition that defines the global parameters generated 
	by the netlister. 

Note that the text block with the ``.control`` block is renamed to ``Text2``. It is 
dumped at the bottom of the netlist file, just before ``.end``. The text block with 
global parameter definitions is named ``Text1`` and is dumped before any elements are netlisted. 

The following toplevel circuit netlist is obtained. 

.. literalinclude:: ../demo/kicad/05-genmmpar/topdc.cir
   :language: none

Demo files for this section can be found `here <../../../demo/kicad/05-genmmpar>`_.

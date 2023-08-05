Customizing netlister behavior with .json files
===============================================
Instead of customizing netlister behavior on a component basis we can do it 
for all components with a selected name from a selected library. 

The default configuration of a Spice Opus netlister for KiCad is defined in 
the :mod:`pyopus.netlister.kicadsocfg` module. You can dump this 
configuration as a .json file by typing::

	python3 -m pyopus.netlister.kicad -d
	
The configuration will be dumped in a window. To dump it to a file named
``netlister.json``, type::

	python3 -m pyopus.netlister.kicad -d -o netlister.json
	
``netlister.json`` is the name of the default netlister configuration file. 
It is written in JSON format. After it is dumped you can customize it and 
it will override the default settings for the library components that are 
specified in this file. It can also be used for customizing general netlister 
behavior. See the :mod:`pyopus.netlister.kicadsocfg` module for details. 
To apply the customizations we did for the Q4 transistor in section 
:ref:`kicad-netlister-fields` to all ``Q_NPN_BEC`` components from the 
``device`` library we write the following ``netlister.json`` file

.. code-block:: none
	
	{
		"Mapping": [
			[
				"device", "Q_NPN_BEC",
				{
					"Parameters": [ "m", "area" ],
					"OutPattern": "#REF() (#PINS()) #MODEL() #PNV() #PV(Specification)",
					"SpiceDevice": "npn",
					"PinMap": [ 3, 1, 2 ],
					"NamePrefix": "Q",
					"ValueField": "Model"
				}
			]
		]
	}

``Mapping`` is a list of lists with 3 elements. The first element is the 
library name, the second one is the component name, and the third one is 
an associative array holding the netlister configuration for the component 
specified by the first two fileds. The entries in this array were explained 
in section :ref:`kicad-netlister-fields`. The ``ValueField`` field 
specifies the name of the field to which the value of the ``Value`` field 
should be copied. In our example we copy it to the ``Model`` filed which 
is used by ``#MODEL()`` in the ``OutPattern``. The model of a Q_NPN_BEC 
can now be specified with the ``Value`` field. If ``ValueField`` is ``null`` 
no copying takes place and the model should be specified via the ``Model`` 
field. 

If one specifies ``null`` for library name and component name the 
corresponding associative array specifies the default netlister configuration 
applied to all components that are not configured explicitly. 

Because KiCad stores copies of library entries in a local cache library the 
netlister will not find the correct mapping entry when a cached copy of 
``Q_NPN_BEC`` is used. Therefore it is recommended to define mapping 
entries with ``null`` as library name. Such entries match a component 
only by its name, regardless of the library where eeschema finds the 
component. With this in mind the above example is more general if it is 
written as 

.. code-block:: none
	
	{
		"Mapping": [
			[
				null, "Q_NPN_BEC",
				{
					"Parameters": [ "m", "area" ],
					"OutPattern": "#REF() (#PINS()) #MODEL() #PNV() #PV(Specification)",
					"SpiceDevice": "npn",
					"PinMap": [ 3, 1, 2 ],
					"NamePrefix": "Q",
					"ValueField": "Model"
				}
			]
		]
	}


``netlister.json`` can also be used to change the behavior of the netlister. 
For instance file

.. literalinclude:: ../demo/kicad/03-netlister-json/netlister.json
   :language: none

specifies that the nodes should be numbered instead of using the 
KiCad-generated net names as basis for node names (``EnumerateNets``), 
the prefix for automatically generated node names should ``net`` 
(``NetPrefix``), the node numbers should be written with at least 3 digits 
(``NetNumbers``), and that the concluding ``.end`` line should be added 
if the netlist is a top-level netlist (``SuppressEnd``), See the 
:mod:`pyopus.netlister.kicadsocfg` module for details. 

File ``netlister.json`` applies to all files generated from intermediate 
XML netlists in the folder where ``netlister.json`` is stored. 
Customization can be applied to individual netlists by naming the file 
``<output netlist file name>.netlister.json``. 

Demo files for this section can be found `here <../../../demo/kicad/03-netlister-json>`_.

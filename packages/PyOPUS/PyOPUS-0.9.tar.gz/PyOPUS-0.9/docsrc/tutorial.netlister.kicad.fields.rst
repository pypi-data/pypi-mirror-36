.. _kicad-netlister-fields:

Customizing netlister behavior with component fields
====================================================
Default netlister behavior can be overridden by adding specific fields to a 
component. Suppose we have the follwing schematic. 

.. figure:: kicad-fields.png
	:scale: 60%
	
	Sample circuits used for demonstrating netlister customization via 
	component fields. 

All transistors are ``Q_NPN_BEC`` components from the ``device`` library. 
Because they are not defined in the default netlister configuration they 
are netlisted as subcircuits (with instance name prefixed by X). The Value 
filed is used as the subcircuit name. 

In Q_NPN_BEC, collector, base, and emitter pins are numbered 3, 1, and 2 
which means that base will be dumped as the first subcircuit pin, emitter 
as the second, and colelctor as the third. Therefore Q1 without any 
special fields defined will be netlisted as

.. code-block:: none

	xq1 (b1 0 c1) T2N2222
	
To netlist the pins in correct order (collector, base, emitter) we add 
a field named PinMap and set it to "3 1 2". This will dump pin number 
3 as the first subcircuit pin (thus collector will come first), followed 
by pins 1 and 2 (base and emitter). Now Q1 will be netlisted as
	
.. code-block:: none

	xq1 (c1 b1 0) T2N2222
	
To netlist it as a builtin bipolar transistor device (without adding the 
x prefix to device name) we must set the NamePrefix field to "Q". This 
is what we did with Q2 which is netlisted as

.. code-block:: none

	q2 (c1 b1 0) T2N2222

To add parameters to the netlisted instance we must define the Parameters 
field and set it to the names of the parameters that will be dumped. The 
values of parameters can be set as additional fileds with parameter name 
for field name and parameter value for field value. To dump parameters 
"area" and "m" we must set the Parameters field to "area m". If we now 
define the "area" and/or the "m" field they will be dumped in the netlist. 
Setting m to 4 and area to 8 (as in transistor Q3) will result in

.. code-block:: none

	q3 (c3 b3 0) T2N2222 param: m=4 area=8
	
Although this is fine for a subcircuit (where keyword "param:") must be 
added it is not OK for a builtin bipolar transistor. To get rid of the 
"param:" keyword we must change the netlisting pattern by defining the 
OutPattern field (as in transistor Q4). By default unknown components 
are netlisted with the following pattern

.. code-block:: none

	#REF() (#PINS()) #MODEL() #PARAM() #PNV() #PV(Specification)
	
This means that first the correctly prefixed component name (``#REF()``) 
is dumped, followed by its pins in parenthesis (``(#PINS())``). Next the 
model name is dumped (``#MODEL()``) which is obtained from the Value field 
followed by the "param:" keyword (``#PARAM()``) which is dumped if any 
of the parameters listed in the Parameters field are defined as fields. 
This is followed by pairs of the form name=value (``#PNV()``). In the end 
the verbatim value of the Specification field (if defined) is added 
(``#PV(Specification)``). 

To get rid of "param:" we drop ``#PARAM()`` from the pattern by setting 
the OutPattern field to 

.. code-block:: none

	#REF() (#PINS()) #MODEL() #PNV() #PV(Specification)

This will dump Q4 which (has all the mentioned customizations) as

.. code-block:: none

	q4 (c4 b4 0) T2N2222 m=4 area=8

which is the correct way for netlisting a builtin bipolar transistor 
device. 

Demo files for this section can be found `here <../../../demo/kicad/02-fields>`_.

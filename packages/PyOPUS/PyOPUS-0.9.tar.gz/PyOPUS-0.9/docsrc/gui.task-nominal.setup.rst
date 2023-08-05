Setting up a nominal design task
================================

Go to the Design tasks tab and add a new task to the Design tasks tree. 
Name it "nominal" and expand the tree item. Select the Requirements 
subitem. For every performance measure defined in the project a 
requirement is added automatically by copying the Above/Below/Norm fields. 
A checkbox is available for every requirement. If it is checked the 
optimizer will try to satisfy the design requirement. Unchecked 
requirements are also evaluated during optimization, but they are not 
affect the optimizer's choice of design parameters. Because we are going 
to design the circuit to satisfy the design requirements arising from 
DC and AC analyses, uncheck requirements overshdn, overshup, tsetdn, 
tsetup, slewdn, slewup, onoise1k, inoise1k, in1kmn2id, in1kmn2rd, and
in1kmn2. 

Also uncheck requirement out_op because it has no lower or upper 
bound specified. If you leave it checked you will get an error message 
when you try to start the task. This is due to the fact that checked 
requirements must have at least one of the two fields Above/Below 
specified. 

Requirements gain_com, gain_vdd, and gain_vss must also be unchecked 
because no design requirements are defined for them. They will still 
be computed, however, because performance measures cmrr, psrr_vdd, and 
psrr_vss depend on them. 

.. figure:: gui-nominal-task-requirements.png
	:scale: 80%
	
	Design requirements setup for the nominal design task. 

The Above and the Below fields specify the lower and the upper bound on 
a performance measure. If a performance measure is a vector this value 
is applied to all of its components. The NMorm field specifies the amount 
by which a design requirement is violated that corresponds to a penalty 
contribution of 1 in the cost function. By default this is equal to 
the greater absolute value of the Above/Below field. If the latter is 
zero, then 1 is used as norm. 

If any of the tradeoff weight fields is specified the optimizer tries to 
optimize those performance measures beyond their design requirements. 
To enable optimization beyond design requirements you must also change 
a setting in the Task settings item. 

Next, open the Parameters item under the newly created task. The parameters 
from the project were automatically copied here

.. figure:: gui-nominal-task-parameters.png
	:scale: 80%
	
	Design parameters setup for the nominal design task. 

Here you specify the initial values and the bounds imposed on the design 
parameters. If you don't want the optimizer to select a value for a 
parameter, clear the Low and the High field. The values specified here 
are used in the task, not the ones that are specified in the project. The 
latter ones are only a template for creating new tasks. 

.. figure:: gui-nominal-task-corner-nominal.png
	:scale: 80%
	
	Adding the "tm" input module to the "nominal" corner
	
A corner named "nominal" was ustomatically added at task creation. It 
comprises nominal operating parameter values and zeros for statistical 
parameter values. We need to add the "tm" input module so that in this 
corner the typical MOS models will be used. 


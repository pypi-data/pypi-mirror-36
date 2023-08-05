Opening plot windows
=============================

PyOPUS provides a wrapper around the MatPlotLib plotting library. The wrapper runs the code 
that refreshes the windows in a separate thread so that the windows remain active during 
computation. After a short prologue that sets up the windows the user can plot within those 
windows using the MatPlotLib API. The resulting figures can be exported in several file 
formats. 

File `01-windows.py <../../../demo/plotting/01-windows.py>`_ 
in folder `demo/plotting/ <../../../demo/plotting>`_

.. literalinclude:: ../demo/plotting/01-windows.py


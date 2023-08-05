Starting the GUI
================

The PyOPUS design automation GUI is started by typing 

.. code-block:: none
  
   pyog

Alternatively you can also type 

.. code-block:: none
  
   python3 -m pyopus.gui.mainwindow
   
The ``pyog`` command has some command line arguments

.. code-block:: none
  
   pyog [project_file.pog|log_file.log|results_file.sqlite]
   
opens a project file, a log, or a results database. Multiple files can 
be specified with the restriction that only one of them can be a project 
file. To get a short help message you can type

.. code-block:: none
  
   pyog -h
   
or 

.. code-block:: none
  
   pyog --help
   

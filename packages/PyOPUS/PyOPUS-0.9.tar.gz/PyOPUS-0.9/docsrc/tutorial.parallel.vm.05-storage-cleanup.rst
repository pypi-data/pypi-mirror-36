Removing old local storage folders
==================================

This demo shows how to delete local storage folders across the cluster using PyOPUS. 

Do not run this demo if there are any PyOPUS tasks running on the cluster because it 
will delete the files in their local storage folders and the tasks will fail. 

File `05-storage-cleanup.py <../../../demo/parallel/vm/05-storage-cleanup.py>`_ 
in folder `demo/parallel/vm/ <../../../demo/parallel/vm/>`_

.. literalinclude:: ../demo/parallel/vm/05-storage-cleanup.py


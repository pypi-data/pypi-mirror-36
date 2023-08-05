Inspecting a results database file from command line
====================================================

The results database of a design task is stored in a SQLite database file. The 
content of this file can be inspected from the command line. The tool for this 
task is the PyOPUS results file inspector (pyori). It can be invoked from the 
command line eqither by typing

.. code-block:: none

   pyori [arguments]

or

.. code-block:: none

   python3 -m pyopus.design.sqlite

If you call it without arguments a short help note will be printed. To print the 
results tree, use 

.. code-block:: none

   pyori <database file.sqlite>
   
To inspect the tree stored in ``corners.sqlite`` one would type

.. code-block:: none

   pyori corners.sqlite tree
   
or simply

.. code-block:: none

   pyori corners.sqlite
     
A typical output looks like

.. code-block:: none

   Children of root record
   -----------------------
   1  : corners (Task, children=7)
   2  :   Aggregator setup (TaskCBD)
   3  :   Pass 1 verification (OptIter)
   4  :   Pass 1 optimization (Corners, children=14)
   5  :     Iteration 1 (OptIter)
   6  :     Iteration 2 (OptIter)
   7  :     Iteration 24 (OptIter)
   8  :     Iteration 66 (OptIter)
   9  :     Iteration 88 (OptIter)
   10 :     Iteration 138 (OptIter)
   11 :     Iteration 187 (OptIter)
   12 :     Iteration 188 (OptIter)
   13 :     Iteration 189 (OptIter)
   14 :     Iteration 239 (OptIter)
   15 :     Iteration 259 (OptIter)
   16 :     Iteration 277 (OptIter)
   17 :     Iteration 291 (OptIter)
   18 :     Iteration 298 (OptIter)
   19 :   Pass 2 verification (OptIter)
   20 :   Pass 2 optimization (Corners, children=9)
   21 :     Iteration 1 (OptIter)
   22 :     Iteration 2 (OptIter)
   23 :     Iteration 20 (OptIter)
   24 :     Iteration 68 (OptIter)
   25 :     Iteration 160 (OptIter)
   26 :     Iteration 161 (OptIter)
   27 :     Iteration 162 (OptIter)
   28 :     Iteration 226 (OptIter)
   29 :     Iteration 289 (OptIter)
   30 :   Pass 3 verification (OptIter)
   31 :   Task summary (Conclusion)

Every row corresponds to one node. Children are indented with respect to their 
parent. Every line starts with the node ID followed by a description. For 
every node the type of the node is printed in parenthesis. For nodes that 
have children the number of children is also printed. 

Every node has one or more aspects associated with it. To print the list of 
aspects available for a particular node, use 

.. code-block:: none

   pyori <database file.sqlite> aspects <node id>
   
To print the list of availabel aspects for node with ID=5, type 

.. code-block:: none

   pyori corners.sqlite aspects 5

To print a particular aspect of a node, type 

.. code-block:: none

   pyori <database file.sqlite> print <node id> <aspect>
   
For instance, to print the ``cost`` aspect of node with ID=5, type

.. code-block:: none

   pyori corners.sqlite print 5 cost
   
The output should look like this. 

.. code-block:: none

   Id      : 5
   Parent  : 4
   Name    : Iteration 1
   Type    : OptIter
   Time    : 1536323228.03 (2018-09-07 14:27:08)
   
        isup < 1.000000e-03   worst=2.371893e-04   cf=0.000000e+00   c8_wp_thi_vhi
     vgs_drv > 0.000000e+00   worst=5.140638e-02   cf=0.000000e+00   c1_wo_tlo_vlo
     vds_drv > 0.000000e+00 o worst=-5.315156e-01  cf=9.712724e-01   c9_ws_tlo_vlo
       swing > 1.000000e+00 o worst=2.228083e-03   cf=9.977719e-01   c11_ws_thi_vlo
        gain > 6.000000e+01 o worst=-8.424399e+01  cf=2.404066e+00   c3_wo_thi_vlo
        ugbw > 1.000000e+07 X in 1 corner(s)       cf=1.000000e+06   c11_ws_thi_vlo
          pm > 5.000000e+01 X in 1 corner(s)       cf=1.000000e+06   c3_wo_thi_vlo
    overshdn < 1.000000e-01 . worst=3.217488e-01   cf=0.000000e+00   c1_wo_tlo_vlo
    overshup < 1.000000e-01 . worst=3.672204e-01   cf=0.000000e+00   c2_wo_tlo_vhi
      tsetdn < 1.000000e-06 . worst=9.995923e-06   cf=0.000000e+00   c3_wo_thi_vlo
      tsetup < 1.000000e-03   worst=9.936220e-06   cf=0.000000e+00   c11_ws_thi_vlo
      slewdn > 2.000000e+06 . worst=5.705511e+03   cf=0.000000e+00   c1_wo_tlo_vlo
      slewup > 2.000000e+06 . worst=7.656355e+02   cf=0.000000e+00   c9_ws_tlo_vlo
        cmrr > 9.000000e+01 o worst=-3.378792e+01  cf=1.375421e+00   c9_ws_tlo_vlo
    psrr_vdd > 6.000000e+01 o worst=-8.438008e+01  cf=2.406335e+00   c3_wo_thi_vlo
    psrr_vss > 6.000000e+01 o worst=-1.961312e+01  cf=1.326885e+00   c9_ws_tlo_vlo
        area < 9.000000e-09   worst=3.961832e-09   cf=0.000000e+00   nominal
   
   cost function value = 2.000009e+06

The node ID, parent's ID, node name, node type, and timepoint are printed 
followed by the desired node's aspect. 

To print all aspects for a particular node, use

.. code-block:: none

   pyori <database file.sqlite> print <node id>

An example:
	
.. code-block:: none

   pyori corners.sqlite print 5
   
would print 

.. code-block:: none

   Id      : 5
   Parent  : 4
   Name    : Iteration 1
   Type    : OptIter
   Time    : 1536323228.03 (2018-09-07 14:27:08)
   
   mirr_w  = 7.469932e-05
   mirr_wd = 9.000483e-05
   mirr_wo = 5.649412e-05
   mirr_l  = 9.164715e-07
   mirr_ld = 2.846626e-06
   out_w   = 4.068112e-05
   out_l   = 1.538790e-06
   load_w  = 2.583243e-06
   load_l  = 1.664465e-06
   diff_w  = 4.843694e-05
   diff_l  = 2.357611e-06
   c_out   = 1.218229e-11
   r_out   = 1.670807e+05
   
   isup     : c8_wp_thi_vhi        =   2.371893e-04 
   vgs_drv  : c1_wo_tlo_vlo [xmn1] =   5.963990e-01 
            :               [xmn2] =   1.864802e-01 
            :               [xmn3] =   5.140638e-02 
            :               [xmn4] =   8.635486e-02 
            :               [xmn5] =   5.140648e-02 
            :               [xmp1] =   9.767202e-01 
            :               [xmp2] =   9.767202e-01 
            :               [xmp3] =   9.586674e-01 
   vds_drv  : c9_ws_tlo_vlo [xmn1] =  -4.038200e-01 Low
            :               [xmn2] =  -3.593675e-02 Low
            :               [xmn3] =   4.920940e-01 
            :               [xmn4] =   9.301180e-02 
            :               [xmn5] =   1.576456e+00 
            :               [xmp1] =   8.820300e-01 
            :               [xmp2] =   8.160324e-01 
            :               [xmp3] =  -5.315156e-01 Low
   swing    : c11_ws_thi_vlo       =   2.228083e-03 Low
   gain     : c3_wo_thi_vlo        =  -8.424399e+01 Low
            : c7_wp_thi_vlo        =  -6.559552e+01 Low
            : c9_ws_tlo_vlo        =  -5.553984e+01 Low
   gain_com : c9_ws_tlo_vlo        =  -2.175192e+01 
   gain_vdd : c3_wo_thi_vlo        =   1.360908e-01 
   gain_vss : c9_ws_tlo_vlo        =  -3.592672e+01 
   ugbw     : c11_ws_thi_vlo       =                Failed
   pm       : c3_wo_thi_vlo        =                Failed
   overshdn : c1_wo_tlo_vlo        =   3.217488e-01 High
   overshup : c2_wo_tlo_vhi        =   3.672204e-01 High
   tsetdn   : c3_wo_thi_vlo        =   9.995923e-06 High
   tsetup   : c11_ws_thi_vlo       =   9.936220e-06 
   slewdn   : c1_wo_tlo_vlo        =   5.705511e+03 Low
   slewup   : c9_ws_tlo_vlo        =   7.656355e+02 Low
   cmrr     : c9_ws_tlo_vlo        =  -3.378792e+01 Low
   psrr_vdd : c3_wo_thi_vlo        =  -8.438008e+01 Low
   psrr_vss : c9_ws_tlo_vlo        =  -1.961312e+01 Low
   area     : nominal              =   3.961832e-09 
   
        isup < 1.000000e-03   worst=2.371893e-04   cf=0.000000e+00   c8_wp_thi_vhi
     vgs_drv > 0.000000e+00   worst=5.140638e-02   cf=0.000000e+00   c1_wo_tlo_vlo
     vds_drv > 0.000000e+00 o worst=-5.315156e-01  cf=9.712724e-01   c9_ws_tlo_vlo
       swing > 1.000000e+00 o worst=2.228083e-03   cf=9.977719e-01   c11_ws_thi_vlo
        gain > 6.000000e+01 o worst=-8.424399e+01  cf=2.404066e+00   c3_wo_thi_vlo
        ugbw > 1.000000e+07 X in 1 corner(s)       cf=1.000000e+06   c11_ws_thi_vlo
          pm > 5.000000e+01 X in 1 corner(s)       cf=1.000000e+06   c3_wo_thi_vlo
    overshdn < 1.000000e-01 . worst=3.217488e-01   cf=0.000000e+00   c1_wo_tlo_vlo
    overshup < 1.000000e-01 . worst=3.672204e-01   cf=0.000000e+00   c2_wo_tlo_vhi
      tsetdn < 1.000000e-06 . worst=9.995923e-06   cf=0.000000e+00   c3_wo_thi_vlo
      tsetup < 1.000000e-03   worst=9.936220e-06   cf=0.000000e+00   c11_ws_thi_vlo
      slewdn > 2.000000e+06 . worst=5.705511e+03   cf=0.000000e+00   c1_wo_tlo_vlo
      slewup > 2.000000e+06 . worst=7.656355e+02   cf=0.000000e+00   c9_ws_tlo_vlo
        cmrr > 9.000000e+01 o worst=-3.378792e+01  cf=1.375421e+00   c9_ws_tlo_vlo
    psrr_vdd > 6.000000e+01 o worst=-8.438008e+01  cf=2.406335e+00   c3_wo_thi_vlo
    psrr_vss > 6.000000e+01 o worst=-1.961312e+01  cf=1.326885e+00   c9_ws_tlo_vlo
        area < 9.000000e-09   worst=3.961832e-09   cf=0.000000e+00   nominal
   
   cost function value = 2.000009e+06

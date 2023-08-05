Trees, tables, and context menus
================================

Data in the GUI is organized in trees and tables. The context menu can be 
obtained with a right-click. The context menu of a tree has the following 
entries:
   
   * Cut - for copying the selection to the clipboard
   * Copy - for copying the selection to the clipboard and then deleting it
   * Paste - for pasting the content of the clipboard at the selected 
     position
   * Select all siblings - for selecting all items in the tree that are 
     siblings of the currently selected item
   * Invert selection - for selecting all unselected siblings of the 
     currently selected items
   * Delete - for deleting the selected items
   * Expand - for expandig the selected items
   * Collapse - for collapsing the selected items
   * Rename - for renaming an item
   * Move up - for moving the selected items up
   * Move down - for moving the selected items down
   * Add item before - for adding an item before the selected item. 
     If it is not clear whether a sibling or a child should be 
     created the GUI opens a dialog and asks you what you want. 
   * Add item after - for adding an item after the selected item. 
     If it is not clear whether a sibling or a child should be 
     created the GUI opens a dialog and asks you what you want. 

Depending on the selection and the nature of the tree some options can be 
disabled. 

.. figure:: gui-context-tree.png
	:scale: 80%
	
	The context menu of a tree. 

Tables also have a context menu with following items:
	
   * Cut - for copying the selection to the clipboard
   * Copy - for copying the selection to the clipboard and then deleting it
   * Paste - for pasting the content of the clipboard at the selected 
     position
   * Select all - for selecting all rows in a table
   * Invert selection - for inverting the selection 
   * Clear cells - for clearing the content of selected cells
   * Remove rows - for removing the rows holding seelcted cells
   * Move rows up - for moving rows with selected cells up
   * Move rows down - for moving rows with selected cells down
   * Add row before - for adding a row before every row with selected cells
   * Add row after - for adding a row after every row with selected cells

Depending on the selection and the nature of the table some options can be 
disabled. 
   
.. figure:: gui-context-table.png
	:scale: 80%
	
	The context menu of a table. 

Single item selection in trees and tables can be made by clicking on an 
item. Multiple items can be selected by holding down ``Ctrl`` and clicking 
items. A range can be selected by clicking on the first item in a range, 
holding ``Shift``, and then clicking the last item in a range. 

   

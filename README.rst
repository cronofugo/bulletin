##########################################
BulletIn: Simple interactive Python prompt
##########################################

BulletIn is an interactive Python prompt to select single or multiple elements from a list. It is a stripped down fork of `bullet <https://github.com/Mckinsey666/bullet>`_.
 
Quick start
***********

Import the bulletin module

.. code-block:: python

   import bulletin

Instantiate a default Dialogs instance

.. code-block:: python

   dialogs = bulletin.Dialogs()

or instantiate a customized Dialogs instance

.. code-block:: python

   dialogs = bulletin.Dialogs(
      shift = 1,
      indent = 3,
      align = 2,
      margin = 1,
      pad_left = 1,
      pad_right = 1,
      check = 'X',
      nocheck = 'O')

Launch a dialog to select only one option

.. code-block:: python

   dialogs.chooseone(
       prompt='Choose the best day:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
       default='Saturday')

or launch a dialog to select one or more options

.. code-block:: python

   dialogs.choosemany(
       prompt='Choose three good days:',
       choices=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
       default=['Monday', 'Wednesday', 'Saturday'])


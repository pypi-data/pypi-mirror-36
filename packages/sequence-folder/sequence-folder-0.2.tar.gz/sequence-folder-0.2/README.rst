sequence-folder
###############

Usage
=====

.. code:: python

   from sequencefolder import SequenceFolder

   a = list('ABCDEFGHI')
   sf = SequenceFolder(a, (3, 3)) # Map the sequence A to a 3x3 array
   print(sf[2][1], sf[2][2], sf[1][0], sf[1][1]) # Prints "H I D E"

   # Preserve mutability
   sf[0][2] = 'A'
   sf[1][0] = 'R'
   sf[2][0] = 'O'
   sf[2][1] = 'O'
   print(''.join(a)) # Prints ABAREFOOI

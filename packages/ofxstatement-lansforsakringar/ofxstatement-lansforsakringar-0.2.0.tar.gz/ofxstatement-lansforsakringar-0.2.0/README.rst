~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Länsförsakringar plugin for ofxstatement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a plug-in for `ofxstatement`_. It converts a bank statement downloaded
from `Länsförsäkringar`_ in XLS (Excel) format to an OFX file suitable for
importing into GnuCash.

.. _ofxstatement: https://github.com/kedder/ofxstatement
.. _länsförsäkringar: https://www.lansforsakringar.se/privat

Usage::

    ofxstatement convert -t lansforsakringar filename.xls filename.ofx

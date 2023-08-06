~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Arbejdernes Landsbank plugin for ofxstatement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a plug-in for `ofxstatement`_. It converts a bank statement downloaded
from `Arbejdernes Landsbank`_ in CSV format to an OFX file suitable for
importing into GnuCash.

.. _ofxstatement: https://github.com/kedder/ofxstatement
.. _arbejdernes landsbank: https://www.al-bank.dk

Note that when generating the CSV file you **must** select the option to
include the column names. The columns can be in any order and any unsupported
or unknown columns are ignored.

The decimal separator can be either dot or comma; both are supported by this
plug-in.

Usage::

    ofxstatement convert -t al_bank filename.csv filename.ofx


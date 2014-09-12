ChemSpiPy
=========

ChemSpiPy provides a way to interact with ChemSpider in Python. It allows chemical searches, chemical file downloads,
depiction and retrieval of chemical properties::

    >>> from chemspipy import ChemSpider
    >>> cs = ChemSpider('<YOUR-SECURITY-TOKEN>')
    >>> c = cs.get_compound('236')  # Specify compound by ChemSpider ID
    >>> c = cs.search('benzene')  # Search using name, SMILES, InChI, InChIKey, etc.

Installation
------------

Install ChemSpiPy using::

    pip install chemspipy

Alternatively, try one of the other `installation options`_.

Documentation
-------------

Full documentation is available at http://chemspipy.readthedocs.org.

Contribute
----------

-  Feature ideas and bug reports are welcome on the `Issue Tracker`_.
-  Fork the `source code`_ on GitHub, make changes and file a pull request.

License
-------

ChemSpiPy is licensed under the `MIT license`_.

This project was originally forked from `ChemSpiPy by Cameron Neylon`_, which has been released into the public domain.

.. _`installation options`: http://chemspipy.readthedocs.org/en/latest/guide/install.html
.. _`source code`: https://github.com/mcs07/ChemSpiPy
.. _`Issue Tracker`: https://github.com/mcs07/ChemSpiPy/issues
.. _`MIT license`: https://github.com/mcs07/ChemSpiPy/blob/master/LICENSE
.. _`ChemSpiPy by Cameron Neylon`: https://github.com/cameronneylon/ChemSpiPy





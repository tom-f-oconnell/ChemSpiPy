.. _misc:

Miscellaneous
=============

.. _datasources:

Data Sources
------------

Get a list of data sources in ChemSpider using the :meth:`~chemspipy.api.ChemSpider.get_datasources` method:

    >>> cs.get_datasources()
    ['Abacipharm', 'Abblis Chemicals', 'Abcam', 'ABI Chemicals', 'Abmole Bioscience', 'ACB Blocks', 'Accela ChemBio', ... ]

Format Conversion
-----------------

Convert between different molecular representations using the :meth:`~chemspipy.api.ChemSpider.convert` method::

    >>> cs.convert('c1ccccc1', 'SMILES', 'InChI')
    'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H'

Allowed conversions:

- From ``InChI`` to ``InChIKey``
- From ``InChI`` to ``Mol``
- From ``InChI`` to ``SMILES``
- From ``InChIKey`` to ``InChI``
- From ``InChIKey`` to ``Mol``
- From ``Mol`` to ``InChI``
- From ``Mol`` to ``InChIKey``
- From ``SMILES`` to ``InChI``

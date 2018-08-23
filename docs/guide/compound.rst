.. _compound:

Compound
========

Many ChemSpiPy search methods return :class:`~chemspipy.objects.Compound` objects, which provide more functionality that
a simple list of ChemSpider IDs. The primary benefit is allowing easy access to further compound properties after
performing a search.

Creating a Compound
-------------------

The easiest way to create a :class:`~chemspipy.objects.Compound` for a given ChemSpider ID is to use the
:meth:`~chemspipy.api.ChemSpider.get_compound` method::

    >>> compound = cs.get_compound(2157)

Alternatively, a :class:`~chemspipy.objects.Compound` can be instantiated directly::

    >>> compound = Compound(cs, 2157)

Either way, no requests are made to the ChemSpider servers until specific :class:`~chemspipy.objects.Compound`
properties are requested::

    >>> print(compound.molecular_formula)
    C_{9}H_{8}O_{4}
    >>> print(compound.molecular_weight)
    180.1574
    >>> print(compound.smiles)
    CC(=O)Oc1ccccc1C(=O)O
    >>> print(compound.common_name)
    Aspirin

Properties are cached locally after the first time they are retrieved, speeding up subsequent access and reducing the
number of unnecessary requests to the ChemSpider servers.

Searching for Compounds
-----------------------

See the :ref:`searching documentation <searching>` for full details.

Implementation details
----------------------

Each :class:`~chemspipy.objects.Compound` object is a simple wrapper around a ChemSpider ID. Behind the scenes, the
property methods use the :meth:`~chemspipy.api.ChemSpider.get_details`, :meth:`~chemspipy.api.ChemSpider.convert`,
:meth:`~chemspipy.api.ChemSpider.get_image`, and :meth:`~chemspipy.api.ChemSpider.get_external_references` API methods
to retrieve the relevant information. It is possible to use these API methods directly if required::

    >>> info = cs.get_details(2157)
    >>> print(info.keys())
    dict_keys(['id', 'smiles', 'formula', 'averageMass', 'molecularWeight', 'monoisotopicMass', 'nominalMass', 'commonName', 'referenceCount', 'dataSourceCount', 'pubMedCount', 'rscCount', 'mol2D', 'mol3D'])
    >>> print(info['smiles'])
    CC(=O)Oc1ccccc1C(=O)O

Results are returned as a python dictionary that is derived directly from the ChemSpider API JSON response.

Compound properties
-------------------

.. class:: chemspipy.objects.Compound
   :noindex:

   .. autoattribute:: record_id
      :noindex:

   .. autoattribute:: image_url
      :noindex:

   .. autoattribute:: molecular_formula
      :noindex:

   .. autoattribute:: inchi
      :noindex:

   .. autoattribute:: inchikey
      :noindex:

   .. autoattribute:: average_mass
      :noindex:

   .. autoattribute:: molecular_weight
      :noindex:

   .. autoattribute:: monoisotopic_mass
      :noindex:

   .. autoattribute:: nominal_mass
      :noindex:

   .. autoattribute:: common_name
      :noindex:

   .. autoattribute:: mol_2d
      :noindex:

   .. autoattribute:: mol_3d
      :noindex:

   .. autoattribute:: image
      :noindex:

   .. autoattribute:: external_references
      :noindex:

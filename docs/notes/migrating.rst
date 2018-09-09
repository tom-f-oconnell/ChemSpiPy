.. _migrating:

Migration Guide
===============

Upgrading to version 2.x
------------------------

The RSC released an entirely new REST API in 2018, necessitating a number of changes to ChemSpiPy. Where possible,
backwards compatibility has been maintained, but many methods are deprecated and some have been removed entirely.

ChemSpider Object
~~~~~~~~~~~~~~~~~

- Instantiate the :class:`~chemspipy.api.ChemSpider` with a required ``api_key`` parameter instead of the optional
  ``security_token`` parameter.

- Deprecated methods:

    - ``get_databases`` → :meth:`~chemspipy.api.ChemSpider.get_datasources`
    - ``get_extended_compound_info`` → :meth:`~chemspipy.api.ChemSpider.get_details`
    - ``get_extended_compound_info_list`` → :meth:`~chemspipy.api.ChemSpider.get_details_batch`
    - ``get_extended_mol_compound_info_list`` → :meth:`~chemspipy.api.ChemSpider.get_details_batch`
    - ``get_record_mol`` → :meth:`~chemspipy.api.ChemSpider.get_mol`
    - ``async_simple_search`` → :meth:`~chemspipy.api.ChemSpider.filter_name`
    - ``async_simple_search_ordered`` → :meth:`~chemspipy.api.ChemSpider.filter_name`
    - ``get_async_search_status`` → :meth:`~chemspipy.api.ChemSpider.filter_status`
    - ``get_async_search_status_and_count`` → :meth:`~chemspipy.api.ChemSpider.filter_status`
    - ``get_async_search_result`` → :meth:`~chemspipy.api.ChemSpider.filter_results`
    - ``get_async_search_result_part`` → :meth:`~chemspipy.api.ChemSpider.filter_results`
    - ``get_compound_info`` → :meth:`~chemspipy.api.ChemSpider.get_details`
    - ``get_compound_thumbnail`` → :meth:`~chemspipy.api.ChemSpider.get_image`
    - ``simple_search`` → :meth:`~chemspipy.api.ChemSpider.search`

- Removed methods:

    - ``get_original_mol``
    - ``get_all_spectra_info``
    - ``get_spectrum_info``
    - ``get_compound_spectra_info``
    - ``get_spectra_info_list``

Compound Object
~~~~~~~~~~~~~~~

- Non-standard InChI and InChIKey are no longer available. All are now 'standard'. Deprecated properties:

    - ``stdinchi`` → :attr:`~chemspipy.objects.Compound.inchi`
    - ``stdinchikey`` → :attr:`~chemspipy.objects.Compound.inchikey`

- Removed properties:

    - ``xlogp``
    - ``alogp``
    - ``mol_3d``
    - ``mol_raw``

Spectrum Object
~~~~~~~~~~~~~~~

- ``Spectrum`` object has been removed entirely.

:mod:`~chemspipy.api` Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Removed ``DIMENSIONS`` mapping.
- Replaced :attr:`~chemspipy.api.FIELDS` mapping with a list of available properties fields.
- Removed ``xml_to_dict`` function.

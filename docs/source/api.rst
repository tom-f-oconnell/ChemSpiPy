.. _api:

API documentation
=================

.. sectionauthor:: Matt Swain <m.swain@me.com>

.. module:: chemspipy

This part of the documentation is automatically generated from the ChemSpiPy source code and comments.

.. automodule:: chemspipy.api
.. autoclass:: chemspipy.ChemSpider()

   .. automethod:: get_compound(csid)
   .. automethod:: get_compounds(csids)
   .. automethod:: get_spectrum(spectrum_id)
   .. automethod:: get_spectra(spectrum_ids)
   .. automethod:: get_compound_spectra(csid)
   .. automethod:: get_all_spectra()
   .. automethod:: search(query, raise_errors=False)
   .. automethod:: search_by_formula(formula)
   .. automethod:: search_by_mass(mass, mass_range)
   .. automethod:: simple_search(query)
   .. automethod:: get_record_mol(csid, calc3d=False)
   .. automethod:: get_original_mol(csid)
   .. automethod:: get_compound_thumbnail(csid)
   .. automethod:: get_databases()
   .. automethod:: get_compound_info(csid)
   .. automethod:: get_extended_compound_info(csid)
   .. automethod:: get_extended_compound_info_list(csids)
   .. automethod:: get_extended_mol_compound_info_list(csids, mol_type=u'e2D', include_reference_counts=False, include_external_references=False)
   .. automethod:: get_compound_spectra_info(csid)
   .. automethod:: get_spectrum_info(spectrum_id)
   .. automethod:: get_spectra_info_list(csids)
   .. automethod:: get_all_spectra_info()
   .. automethod:: request(api, endpoint, **params)
   .. automethod:: construct_api_url(api, endpoint, **params)
   .. automethod:: async_simple_search(query)
   .. automethod:: async_simple_search_ordered(query, order=u'csid', direction=u'ascending')
   .. automethod:: get_async_search_status(rid)
   .. automethod:: get_async_search_status_and_count(rid)
   .. automethod:: get_async_search_result(rid)
   .. automethod:: get_async_search_result_part(rid, start=0, count=-1)

.. automodule:: chemspipy.objects
.. autoclass:: chemspipy.Compound()
   :members:
.. autoclass:: chemspipy.Spectrum()
   :members:

.. automodule:: chemspipy.search
.. autoclass:: chemspipy.Results()
   :members:

.. automodule:: chemspipy.errors
.. autoexception:: chemspipy.errors.ChemSpiPyError()
.. autoexception:: chemspipy.errors.ChemSpiPyParseError()
.. autoexception:: chemspipy.errors.ChemSpiPyAuthError()
.. autoexception:: chemspipy.errors.ChemSpiPyNotFoundError()
.. autoexception:: chemspipy.errors.ChemSpiPyTimeoutError()
.. autoexception:: chemspipy.errors.ChemSpiPyServerError()

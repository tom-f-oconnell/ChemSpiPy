.. _searching:

Searching
=========

ChemSpiPy provides a number of different ways to search ChemSpider.

Compound search
---------------

The main ChemSpiPy search method functions in a similar way to the main search box on the ChemSpider website. Just
provide any type of query, and ChemSpider will interpret it and provide the most relevant results::

    >>> cs.search('O=C(OCC)C')
    Results([Compound(8525)])
    >>> cs.search('glucose')
    Results([Compound(5589), Compound(58238), Compound(71358), Compound(96749), Compound(2006622), Compound(5341883), Compound(5360239), Compound(9129332), Compound(9281077), Compound(9312824), Compound(9484839), Compound(9655623)])
    >>> cs.search('2157')
    Results([Compound(2157)])

The supported query types include systematic names, synonyms, trade names, registry numbers, molecular formula, SMILES,
InChI and InChIKey.

The :class:`~chemspipy.search.Results` object that is returned can be treated just like any regular python list. For
example, you can iterate over the results::

    >>> for result in cs.search('Glucose'):
    ...    print(result.record_id)
    5589
    58238
    71358
    96749
    2006622
    5341883
    5360239
    9129332
    9281077
    9312824
    9484839
    9655623

The :class:`~chemspipy.search.Results` object also provides the time taken to perform the search, and a message that
explains how the query type was resolved::

    >>> r = cs.search('Glucose')
    >>> print(r.duration)
    0:00:00.513406
    >>> print(r.message)
    Found by approved synonym

Asynchronous searching
----------------------

Certain types of search can sometimes take slightly longer, which can be inconvenient if the search method blocks the
Python interpreter until the search results are returned. Fortunately, the ChemSpiPy search method works asynchronously.

Once a search is executed, ChemSpiPy immediately returns the :class:`~chemspipy.search.Results` object, which is
actually empty at first::

    >>> results = cs.search('O=C(OCC)C')
    >>> print(results.ready())
    False

In a background thread, ChemSpiPy is making the search request and waiting for the response. But in the meantime, it is
possible to continue performing other tasks in the main Python interpreter process. Call
:meth:`~chemspipy.search.Results.ready()` at any point to check if the results have been returned and are available.

Any attempt to access the results will just block until the results are ready, like a simple synchronous search. To
manually block the main thread until the results are ready, use the :meth:`~chemspipy.search.Results.wait()` method::

    >>> results.wait()
    >>> results.ready()
    True

For more detailed information about the status of a search, use the :attr:`~chemspipy.search.Results.status` property::

    >>> results.status
    'Created'
    >>> results.wait()
    >>> results.status
    'Complete'

The possible statuses are ``Created``, ``Failed``, ``Unknown``, ``Suspended``, ``Complete``.

Search by formula
-----------------

Searching by molecular formula is supported by the main :meth:`~chemspipy.api.ChemSpider.search()` method, but there is
the possibility that a formula could be interpreted as a name or SMILES or another query type. To specifically search
by formula, use::

    >>> cs.search_by_formula('C44H30N4Zn')
    [Compound(436642), Compound(3232330), Compound(24746832), Compound(26995124)]

Search by mass
--------------

It is also possible to search ChemSpider by mass by specifying a certain range::

    >>> cs.search_by_mass(680, 0.001)
    [Compound(8298180), Compound(12931939), Compound(12931969), Compound(21182158)]

The first parameter specifies the desired molecular mass, while the second parameter specifies the allowed ± range of
values.

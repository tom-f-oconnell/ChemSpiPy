.. _compound:

Compound
========

TODO

- Many methods return Compound objects
- This is a simple wrapper around a ChemSpider ID that allows further information to be retrieved
- Once retrieved, properties are cached so subsequent access on the same Compound object should be faster.
- Behind the scenes, Compound objects just use other API endpoints:
    - get_extended_compound_info
    - get_record_mol
    - get_compound_thumbnail

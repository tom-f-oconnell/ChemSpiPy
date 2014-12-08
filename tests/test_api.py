# -*- coding: utf-8 -*-
"""
test_api
~~~~~~~~

Test the core API functionality.

:copyright: Copyright 2014 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import logging
import os
import re

import nose
from nose.tools import eq_, ok_, raises
import six

from chemspipy import ChemSpider
from chemspipy.errors import ChemSpiPyAuthError, ChemSpiPyServerError


logging.basicConfig(level=logging.WARN)
logging.getLogger('chemspipy').setLevel(logging.DEBUG)

# Security token is retrieved from environment variables
CHEMSPIDER_SECURITY_TOKEN = os.environ['CHEMSPIDER_SECURITY_TOKEN']

# Chemspider instances with and without a security token
cs = ChemSpider(security_token=CHEMSPIDER_SECURITY_TOKEN)
cs2 = ChemSpider()


def test_no_security_token():
    """Test ChemSpider can be initialized with no parameters."""
    eq_(cs2.security_token, None)


def test_security_token():
    """Test security token is set correctly when initializing ChemSpider"""
    eq_(cs.security_token, CHEMSPIDER_SECURITY_TOKEN)


# MassSpecAPI

def test_get_databases():
    """Test get_databases returns the list of ChemSpider data sources."""
    dbs = cs.get_databases()
    ok_(all(source in dbs for source in ['Wikipedia', 'ZINC', 'PubChem']))


def test_get_extended_compound_info():
    """Test get_extended_compound_info returns info for a CSID."""
    info = cs.get_extended_compound_info(263)
    ok_(all(field in info for field in ['csid', 'molecular_formula', 'smiles', 'inchi', 'inchikey', 'average_mass',
                                        'molecular_weight', 'monoisotopic_mass', 'nominal_mass', 'alogp', 'xlogp',
                                        'common_name']))
    ok_(all(isinstance(info[field], float) for field in ['average_mass', 'molecular_weight', 'monoisotopic_mass',
                                                         'nominal_mass', 'alogp', 'xlogp']))
    ok_(isinstance(info['csid'], int))
    ok_(all(isinstance(info[field], six.text_type) for field in ['molecular_formula', 'smiles', 'inchi', 'inchikey',
                                                                 'common_name']))


def test_get_extended_compound_info_list():
    """Test get_extended_compound_info_list returns info for a list of CSIDs."""
    info = cs.get_extended_compound_info_list([263, 1235, 6084])
    eq_(len(info), 3)
    ok_(all(field in info[0] for field in ['csid', 'molecular_formula', 'smiles', 'inchi', 'inchikey', 'average_mass',
                                        'molecular_weight', 'monoisotopic_mass', 'nominal_mass', 'alogp', 'xlogp',
                                        'common_name']))
    ok_(all(isinstance(info[0][field], float) for field in ['average_mass', 'molecular_weight', 'monoisotopic_mass',
                                                         'nominal_mass', 'alogp', 'xlogp']))
    ok_(isinstance(info[0]['csid'], int))
    ok_(all(isinstance(info[0][field], six.text_type) for field in ['molecular_formula', 'smiles', 'inchi', 'inchikey',
                                                                 'common_name']))


def test_get_extended_mol_compound_info_list():
    """Test get_extended_mol_compound_info_list returns info for a list of CSIDs."""
    info = cs.get_extended_mol_compound_info_list([1236], include_external_references=True,
                                                  include_reference_counts=True)
    eq_(len(info), 1)
    ok_(all(field in info[0] for field in ['csid', 'molecular_formula', 'smiles', 'inchi', 'inchikey', 'average_mass',
                                        'molecular_weight', 'monoisotopic_mass', 'nominal_mass', 'alogp', 'xlogp',
                                        'common_name', 'reference_count', 'datasource_count', 'mol_2d']))
    ok_(all(isinstance(info[0][field], float) for field in ['average_mass', 'molecular_weight', 'monoisotopic_mass',
                                                         'nominal_mass', 'alogp', 'xlogp']))
    ok_(all(isinstance(info[0][field], int) for field in ['csid', 'reference_count', 'datasource_count']))
    ok_(all(isinstance(info[0][field], six.text_type) for field in ['molecular_formula', 'smiles', 'inchi', 'inchikey',
                                                                 'common_name', 'mol_2d']))


def test_get_extended_mol_compound_info_list_dimensions():
    """Test get_extended_mol_compound_info_list returns 2D/3D/both MOL."""
    info = cs.get_extended_mol_compound_info_list([1236], mol_type='2d')
    ok_('mol_2d' in info[0])
    info = cs.get_extended_mol_compound_info_list([1236], mol_type='3d')
    ok_('mol_3d' in info[0])
    info = cs.get_extended_mol_compound_info_list([1236], mol_type='both')
    ok_('mol_2d' in info[0])
    ok_('mol_3d' in info[0])


def test_get_record_mol():
    """Test get_record_mol returns a MOL file."""
    mol = cs.get_record_mol(6084)
    ok_('V2000' in mol)
    ok_('M  END' in mol)


def test_search_by_formula():
    """Test search_by_formula returns a list of CSIDs."""
    eq_([c.csid for c in cs.search_by_formula('C2H6')], [6084])


def test_search_by_mass():
    """Test search_by_mass returns a list of CSIDs."""
    csids = [c.csid for c in cs.search_by_mass(17, 0.1)]
    ok_(all(csid in csids for csid in [217, 936, 12148, 94766, 138477, 4925349, 8305396, 8466194, 9237452, 21864986]))


# Search

def test_async_simple_search():
    """Test async_simple_search returns a transaction ID."""
    rid = cs.async_simple_search('benzene')
    ok_(re.compile(r'[a-f0-9\-]{20,50}').search(rid))


def test_async_simple_search_ordered():
    """Test async_simple_search returns a transaction ID."""
    rid = cs.async_simple_search_ordered('glucose')
    ok_(re.compile(r'[a-f0-9\-]{20,50}').search(rid))


def test_get_async_search_status():
    """Test get_async_search_status returns the status for a transaction ID."""
    rid = cs.async_simple_search('benzene')
    status = cs.get_async_search_status(rid)
    ok_(status in {'Unknown', 'Created', 'Scheduled', 'Processing', 'Suspended', 'PartialResultReady', 'ResultReady'})


def test_get_async_search_status_and_count():
    """Test get_async_search_status_and_count returns the status for a transaction ID."""
    rid = cs.async_simple_search('benzene')
    while True:
        status = cs.get_async_search_status_and_count(rid)
        if status['status'] in {'Created', 'Scheduled', 'Processing'}:
            continue
        eq_(status['count'], 1)
        eq_(status['message'], 'Found by approved synonym')
        break


def test_get_async_search_result():
    """Test get_async_search_result returns a list of CSIDs."""
    rid = cs.async_simple_search('benzene')
    while True:
        status = cs.get_async_search_status(rid)
        if status in {'Created', 'Scheduled', 'Processing'}:
            continue
        eq_([c.csid for c in cs.get_async_search_result(rid)], [236])
        break


def test_get_async_search_result_part():
    """Test get_async_search_result_part returns a list of CSIDs."""
    rid = cs.async_simple_search('glucose')
    while True:
        status = cs.get_async_search_status(rid)
        if status in {'Created', 'Scheduled', 'Processing'}:
            continue
        eq_([c.csid for c in cs.get_async_search_result_part(rid)], [5589, 58238, 71358, 96749, 9312824, 9484839])
        eq_([c.csid for c in cs.get_async_search_result_part(rid, start=2)], [71358, 96749, 9312824, 9484839])
        eq_([c.csid for c in cs.get_async_search_result_part(rid, start=2, count=2)], [71358, 96749])
        eq_([c.csid for c in cs.get_async_search_result_part(rid, start=2, count=99)], [71358, 96749, 9312824, 9484839])
        break


def test_get_compound_info():
    """Test get_compound_info returns info for a CSID."""
    info = cs.get_compound_info(263)
    ok_(all(field in info for field in ['csid', 'smiles', 'inchi', 'inchikey']))
    ok_(isinstance(info['csid'], int))
    ok_(all(isinstance(info[field], six.text_type) for field in ['smiles', 'inchi', 'inchikey']))


def test_get_compound_thumbnail():
    """Test get_compound_thumbnail returns image data for a CSID."""
    img = cs.get_compound_thumbnail(263)
    eq_(img[:8], b'\x89PNG\x0d\x0a\x1a\x0a')  # PNG magic number


def test_simple_search():
    """Test simple_search returns a list of CSIDs."""
    eq_([c.csid for c in cs.simple_search('glucose')], [5589, 58238, 71358, 96749, 9312824, 9484839])


# Spectra

def test_get_spectra_info_list():
    """Test get_spectra_info_list returns spectra info for a list of CSIDs."""
    spectra = cs.get_spectra_info_list([6084])
    eq_(spectra[0]['csid'], 6084)
    eq_(cs.get_spectra_info_list([263]), [])  # No spectra for this compound


# InChI

def test_get_original_mol():
    """Test get_original_mol returns a MOL file."""
    mol = cs.get_original_mol(6084)
    ok_('V2000' in mol)
    ok_('M  END' in mol)



# Errors

@raises(ChemSpiPyAuthError)
def test_token_needed():
    """Test ChemSpiPyAuthError is raised for certain endpoints if no security_token provided."""
    cs2.get_extended_compound_info(263)


@raises(ChemSpiPyServerError)
def test_token_needed():
    """Test ChemSpiPyServerError is raised when an invalid transaction ID is used."""
    cs.get_async_search_status('xxxxxx')


@raises(ChemSpiPyServerError)
def test_token_needed():
    """Test ChemSpiPyServerError is raised when a valid but expired transaction ID is used."""
    cs.get_async_search_status('1a93ee87-acbe-4caa-bc3b-23c3ff39be0f')


@raises(ChemSpiPyServerError)
def test_token_needed():
    """Test ChemSpiPyServerError is raised when a valid but made up transaction ID is used."""
    cs.get_async_search_status('1a93ee87-acbe-4caa-bc3b-23c3ff39be0a')


if __name__ == '__main__':
    nose.main()

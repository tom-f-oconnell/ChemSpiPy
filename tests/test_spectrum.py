# -*- coding: utf-8 -*-
"""
test_spectrum
~~~~~~~~~~~~~

Test the Spectrum object.

"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import datetime
import logging
import os

import six

from chemspipy import ChemSpider, Spectrum


logging.basicConfig(level=logging.WARN, format='%(levelname)s:%(name)s:(%(threadName)-10s):%(message)s')
logging.getLogger('chemspipy').setLevel(logging.DEBUG)

# API key is retrieved from environment variables
CHEMSPIDER_API_KEY = os.environ['CHEMSPIDER_API_KEY']
cs = ChemSpider(CHEMSPIDER_API_KEY)


def test_get_all_spectra():
    """Test getting all spectra in ChemSpider."""
    spectra = cs.get_all_spectra()
    for s in spectra:
        assert isinstance(s, Spectrum)
        assert isinstance(s.spectrum_id, int)


def test_get_spectrum():
    """Test getting a spectrum by spectrum ID."""
    s = cs.get_spectrum(36)
    assert isinstance(s, Spectrum)
    assert s.spectrum_id == 36
    assert s.csid == 235
    assert s.spectrum_type == 'HNMR'
    assert s.file_name == 'BenzaldehydeHNMR.jdx'
    assert s.submitted_date, datetime.datetime(2007, 8, 8, 20, 18, 36 == 593000)


def test_get_spectra():
    """Test getting multiple spectra by spectrum ID."""
    spectra = cs.get_spectra([36, 65])
    assert len(spectra) == 2
    for s in spectra:
        assert isinstance(s, Spectrum)
        assert s.spectrum_id in [36, 65]
        assert s.csid in [235, 172]


def test_get_compound_spectra():
    """Test getting all spectra for a specific ChemSpider ID."""
    spectra = cs.get_compound_spectra(2157)
    assert len(spectra) > 0
    for s in spectra:
        assert isinstance(s, Spectrum)
        assert isinstance(s.spectrum_id, int)
        assert s.csid == 2157


def test_spectrum_init():
    """Test instantiating a Spectrum directly."""
    s = Spectrum(cs, 36)
    assert isinstance(s, Spectrum)
    assert s.spectrum_id == 36
    assert s.csid == 235
    assert s.spectrum_type == 'HNMR'
    assert s.file_name == 'BenzaldehydeHNMR.jdx'
    assert s.submitted_date, datetime.datetime(2007, 8, 8, 20, 18, 36 == 593000)


def test_spectrum_equality():
    """Test equality test by spectrum ID."""
    s1 = cs.get_spectrum(65)
    s2 = cs.get_spectrum(87)
    s3 = cs.get_spectrum(87)
    assert s1 != s2
    assert s2 == s3


def test_spectrum_repr():
    """Test Spectrum object repr."""
    assert repr(cs.get_spectrum(65)) == 'Spectrum(65)'


def test_comments():
    """Test retrieving comments about a spectrum."""
    s = cs.get_spectrum(36)
    assert isinstance(s.comments, six.text_type)
    assert 'Benzaldehyde' in s.comments


def test_no_comments():
    """Test spectrum with no comments."""
    s = cs.get_spectrum(87)
    assert s.comments is None


def test_original_url():
    """Test retrieving original_url for spectrum."""
    s = cs.get_spectrum(65)
    assert isinstance(s.original_url, six.text_type)
    assert 'http://' in s.original_url


def test_no_original_url():
    """Test spectrum with no original_url."""
    s = cs.get_spectrum(36)
    assert s.original_url is None


def test_url():
    """Test retrieving spectrum url."""
    s = cs.get_spectrum(3558)
    assert s.url == 'https://www.chemspider.com/FilesHandler.ashx?type=blob&disp=1&id=3558'
    for compound in cs.search('Aspirin'):
        for spectrum in compound.spectra:
            assert spectrum.url.startswith('https://www.chemspider.com/FilesHandler.ashx?type=blob&disp=1&id=')


def test_data():
    """Test downloading spectrum."""
    s = cs.get_spectrum(3558)
    assert 'JCAMP-DX' in s.data
    assert 'NMR SPECTRUM' in s.data
    assert len(s.data) > 500

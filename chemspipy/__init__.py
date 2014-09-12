# -*- coding: utf-8 -*-
"""
ChemSpiPy
~~~~~~~~~

Python wrapper for the ChemSpider API.

:copyright: Copyright 2014 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division


__author__ = 'Matt Swain'
__email__ = 'm.swain@me.com'
__version__ = '1.0.0'
__license__ = 'MIT'


from .api import ChemSpider
from .objects import Compound
from .search import Results

# -*- coding: utf-8 -*-
"""
chemspipy.api
~~~~~~~~~~~~~

Core API for interacting with ChemSpider web services.

"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from base64 import b64decode
import logging
import sys
import warnings

import requests
import six

from . import __version__, errors
from .objects import Compound
from .search import Results


log = logging.getLogger(__name__)


#: Default API URL.
API_URL = 'https://api.rsc.org'
#: Default API version.
API_VERSION = 'v1'

#: 2D coordinate dimensions
MOL2D = '2d'
#: 3D coordinate dimensions
MOL3D = '3d'
#: Both coordinate dimensions
BOTH = 'both'

#: Ascending sort direction
ASCENDING = 'ascending'
#: Descending sort direction
DESCENDING = 'descending'

#: CSID sort order
CSID = 'csid'
#: Mass defect sort order
MASS_DEFECT = 'mass_defect'
#: Molecular weight sort order
MOLECULAR_WEIGHT = 'molecular_weight'
#: Reference count sort order
REFERENCE_COUNT = 'reference_count'
#: Datasource count sort order
DATASOURCE_COUNT = 'datasource_count'
#: Pubmed count sort order
PUBMED_COUNT = 'pubmed_count'
#: RSC count sort order
RSC_COUNT = 'rsc_count'


#: Coordinate dimensions
DIMENSIONS = {
    MOL2D: 'e2D',
    MOL3D: 'e3D',
    BOTH: 'eBoth'
}

#: Sort directions
DIRECTIONS = {
    ASCENDING: 'eAscending',
    DESCENDING: 'eDescending'
}

#: Sort orders
ORDERS = {
    CSID: 'eCSID',
    MASS_DEFECT: 'eMassDefect',
    MOLECULAR_WEIGHT: 'eMolecularWeight',
    REFERENCE_COUNT: 'eReferenceCount',
    DATASOURCE_COUNT: 'eDataSourceCount',
    PUBMED_COUNT: 'ePubMedCount',
    RSC_COUNT: 'eRscCount'
}

#: API to python field mappings
FIELDS = {
    'CSID': ('csid', int),
    'csid': ('csid', int),
    'MF': ('molecular_formula', six.text_type),
    'SMILES': ('smiles', six.text_type),
    'InChI': ('inchi', six.text_type),
    'InChIKey': ('inchikey', six.text_type),
    'AverageMass': ('average_mass', float),
    'MolecularWeight': ('molecular_weight', float),
    'MonoisotopicMass': ('monoisotopic_mass', float),
    'NominalMass': ('nominal_mass', float),
    'ALogP': ('alogp', float),
    'XLogP': ('xlogp', float),
    'CommonName': ('common_name', six.text_type),
    'MOL2d': ('mol_2d', six.text_type),
    'MOL3d': ('mol_3d', six.text_type),
    'ReferenceCount': ('reference_count', int),
    'DataSourceCount': ('datasource_count', int),
    'PubMedCount': ('pubmed_count', int),
    'RSCCount': ('rsc_count', int),
    'ExternalReferences': ('external_references', list),
    'ds_name': ('datasource_name', six.text_type),
    'ds_url': ('datasource_url', six.text_type),
    'ext_id': ('external_id', six.text_type),
    'ext_url': ('external_url', six.text_type),
    'Status': ('status', six.text_type),
    'Count': ('count', int),
    'Message': ('message', six.text_type),
    'Elapsed': ('elapsed', six.text_type),
    'spc_id': ('spectrum_id', int),
    'spc_type': ('spectrum_type', six.text_type),
    'file_name': ('file_name', six.text_type),
    'comments': ('comments', six.text_type),
    'original_url': ('original_url', six.text_type),
    'submitted_date': ('submitted_date', six.text_type),
}


class BaseChemSpider(object):

    def __init__(self, api_key, user_agent=None, api_url=API_URL, api_version=API_VERSION):
        """

        :param string api_key: Your ChemSpider API key.
        :param string user_agent: (Optional) Identify your application to ChemSpider servers.
        :param string api_url: (Optional) API server. Default https://api.rsc.org.
        :param string api_version: (Optional) API version. Default v1.
        """
        log.debug('Initializing ChemSpider')
        self.api_url = api_url
        self.http = requests.session()
        self.http.headers['User-Agent'] = user_agent if user_agent else 'ChemSpiPy/{} Python/{} '.format(__version__, sys.version.split()[0])
        self.api_key = api_key
        self.api_version = api_version

    def request(self, method, api, namespace, endpoint, params=None, json=None):
        """Make a request to the ChemSpider API.

        :param string method: HTTP method.
        :param string api: Top-level API, e.g. compounds.
        :param string namespace: API namespace, e.g. filter, lookups, records, or tools.
        :param string endpoint: Web service endpoint URL.
        :param dict params: Query parameters to add to the URL.
        :param dict json: JSON data to send in the request body.
        :return: Web Service response JSON.
        :rtype: dict
        """
        # Construct request URL
        url = '{}/{}/{}/{}/{}'.format(self.api_url, api, self.api_version, namespace, endpoint)

        # Set apikey header
        headers = {'apikey': self.api_key}

        log.debug('{} : {} : {} : {}'.format(url, headers, params, json))

        # Make request
        r = self.http.request(method, url, params=params, json=json, headers=headers)

        # Raise exception for HTTP errors
        if not r.ok:
            err = {
                400: errors.ChemSpiPyBadRequestError,
                401: errors.ChemSpiPyAuthError,
                404: errors.ChemSpiPyNotFoundError,
                405: errors.ChemSpiPyMethodError,
                413: errors.ChemSpiPyPayloadError,
                429: errors.ChemSpiPyRateError,
                500: errors.ChemSpiPyServerError,
                503: errors.ChemSpiPyUnavailableError
            }.get(r.status_code, errors.ChemSpiPyHTTPError)
            raise err(message=r.reason, http_code=r.status_code)

        log.debug('Request duration: {}'.format(r.elapsed))
        return r.json()

    def get(self, api, namespace, endpoint, params=None):
        """Convenience method for making GET requests.

        :param string api: Top-level API, e.g. compounds.
        :param string namespace: API namespace, e.g. filter, lookups, records, or tools.
        :param string endpoint: Web service endpoint URL.
        :param dict params: Query parameters to add to the URL.
        :return: Web Service response JSON.
        :rtype: dict
        """
        return self.request('GET', api=api, namespace=namespace, endpoint=endpoint, params=params)

    def post(self, api, namespace, endpoint, json=None):
        """Convenience method for making POST requests.

        :param string api: Top-level API, e.g. compounds.
        :param string namespace: API namespace, e.g. filter, lookups, records, or tools.
        :param string endpoint: Web service endpoint URL.
        :param dict json: JSON data to send in the request body.
        :return: Web Service response content.
        :rtype: dict or string
        """
        return self.request('POST', api=api, namespace=namespace, endpoint=endpoint, json=json)


def xml_to_dict(t):
    """Convert a ChemSpider XML response to a python dict."""
    d = {}
    for child in t:
        tag = child.tag.split('}')[1]
        tag, rtype = FIELDS.get(tag, (tag, six.text_type))
        if rtype == list:
            d[tag] = [xml_to_dict(grandchild) for grandchild in child]
        elif rtype == dict:
            d[tag] = xml_to_dict(child)
        elif child.text is not None:
            d[tag] = rtype(child.text.strip())
    return d


class LookupsApi(BaseChemSpider):
    """"""

    def get_datasources(self):
        """Get the list of datasources in ChemSpider.

        Many other endpoints let you restrict which sources are used to lookup the requested query. Restricting the
        sources makes queries faster.

        :return: List of datasources.
        :rtype: list[string]
        """
        response = self.get(api='compounds', namespace='lookups', endpoint='datasources')
        return response['dataSources']


class RecordsApi(BaseChemSpider):
    """"""

    def get_details(self, record_id, fields=None):
        """Get details for a compound record.

        The available fields are: SMILES, Formula, AverageMass, MolecularWeight, MonoisotopicMass, NominalMass,
        CommonName, ReferenceCount, DataSourceCount, PubMedCount, RSCCount, Mol2D, Mol3D.

        :param int record_id: Record ID.
        :param list[string] fields: List of fields to include in the result.
        :return: Record details.
        :rtype: dict
        """
        # Use all fields if none are specified
        if fields is None:
            fields = [
                'SMILES', 'Formula', 'AverageMass', 'MolecularWeight', 'MonoisotopicMass', 'NominalMass', 'CommonName',
                'ReferenceCount', 'DataSourceCount', 'PubMedCount', 'RSCCount', 'Mol2D', 'Mol3D'
            ]
        params = {'fields': ','.join(fields)}
        endpoint = '{}/details'.format(record_id)
        response = self.get(api='compounds', namespace='records', endpoint=endpoint, params=params)
        return response

    def get_details_batch(self, record_ids, fields=None):
        """Get details for a list of compound records.

        The available fields are: SMILES, Formula, AverageMass, MolecularWeight, MonoisotopicMass, NominalMass,
        CommonName, ReferenceCount, DataSourceCount, PubMedCount, RSCCount, Mol2D, Mol3D.

        :param list[int] record_ids: List of record IDs (up to 100).
        :param list[string] fields: List of fields to include in the results.
        :return: List of record details.
        :rtype: list[dict]
        """
        # Use all fields if none are specified
        if fields is None:
            fields = [
                'SMILES', 'Formula', 'AverageMass', 'MolecularWeight', 'MonoisotopicMass', 'NominalMass', 'CommonName',
                'ReferenceCount', 'DataSourceCount', 'PubMedCount', 'RSCCount', 'Mol2D', 'Mol3D'
            ]
        json = {'recordIds': record_ids, 'fields': fields}
        response = self.post(api='compounds', namespace='records', endpoint='batch', json=json)
        return response['records']

    def get_external_references(self, record_id, datasources=None):
        """Get external references for a compound record.

        Optionally filter the results by data source. Use :meth:`~chemspipy.api.ChemSpider.get_datasources` to get the
        available datasources.

        :param int record_id: Record ID.
        :param list[string] datasources: List of datasources to restrict the results to.
        :return: External references.
        :rtype: list[string]
        """
        params = {}
        if datasources is not None:
            params['dataSources'] = ','.join(datasources)
        endpoint = '{}/externalreferences'.format(record_id)
        response = self.get(api='compounds', namespace='records', endpoint=endpoint, params=params)
        return response['externalReferences']

    def get_image(self, record_id):
        """Get image for a compound record.

        :param int record_id: Record ID.
        :return: Image.
        :rtype: bytes
        """
        endpoint = '{}/image'.format(record_id)
        response = self.get(api='compounds', namespace='records', endpoint=endpoint)
        return b64decode(response['image'])

    def get_mol(self, record_id):
        """Get MOLfile for a compound record.

        :param int record_id: Record ID.
        :return: MOLfile.
        :rtype: string
        """
        endpoint = '{}/mol'.format(record_id)
        response = self.get(api='compounds', namespace='records', endpoint=endpoint)
        return response['sdf']


class FilterApi(BaseChemSpider):
    """"""

    def filter_name(self, name, order_by=None, order_direction=None):
        """Search by compound name.

        Valid values for orderBy are recordId, massDefect, molecularWeight, referenceCount, dataSourceCount,
        pubMedCount, rscCount.

        Valid values for orderDirection are ascending, descending.

        :param string name: Compound name.
        :param string order_by: What to sort the results by.
        :param string order_direction: Ascending or descending sort direction for results.
        :return:
        """
        json = {'name': name, 'orderBy': order_by, 'orderDirection': order_direction}
        response = self.post(api='compounds', namespace='filter', endpoint='name', json=json)
        return response['queryId']

    def get_results(self, query_id, start=None, count=None):
        """Get filter results using a query ID that was returned by a previous filter requests.

        :param query_id: Query ID from a previous filter request.
        :param int start: Zero-based results offset.
        :param int count: Number of results to return.
        :return: List of results.
        :rtype: list[int]
        """
        endpoint = '{}/results'.format(query_id)
        params = {'start': start, 'count': count}
        response = self.get(api='compounds', namespace='filter', endpoint=endpoint, params=params)
        return response['sdf']


class MassSpecApi(BaseChemSpider):

    def get_databases(self):
        """Get the list of datasources in ChemSpider."""
        warnings.warn('Use get_datasources instead of get_databases.', DeprecationWarning)
        return self.get_datasources()

    def get_extended_compound_info(self, csid):
        """Get extended record details for a CSID. Security token is required.

        :param string|int csid: ChemSpider ID.
        """
        warnings.warn('Use get_details instead of get_extended_compound_info.', DeprecationWarning)
        return self.get_details(record_id=csid)

    def get_extended_compound_info_list(self, csids):
        """Get extended record details for a list of CSIDs. Security token is required.

        :param list[string|int] csids: ChemSpider IDs.
        """
        warnings.warn('Use get_details_batch instead of get_extended_compound_info.', DeprecationWarning)
        return self.get_details_batch(record_ids=csids)

    def get_extended_mol_compound_info_list(self, csids, mol_type=MOL2D, include_reference_counts=False,
                                            include_external_references=False):
        """Get extended record details (including MOL) for a list of CSIDs.

        A maximum of 250 CSIDs can be fetched per request. Security token is required.

        :param list[string|int] csids: ChemSpider IDs.
        :param string mol_type: :data:`~chemspipy.api.MOL2D`, :data:`~chemspipy.api.MOL3D` or
                                :data:`~chemspipy.api.BOTH`.
        :param bool include_reference_counts: Whether to include reference counts.
        :param bool include_external_references: Whether to include external references.
        """
        warnings.warn('Use get_details_batch instead of get_extended_mol_compound_info_list.', DeprecationWarning)
        return self.get_details_batch(record_ids=csids)

    def get_record_mol(self, csid, calc3d=False):
        """Get ChemSpider record in MOL format. Security token is required.

        :param string|int csid: ChemSpider ID.
        :param bool calc3d: Whether 3D coordinates should be calculated before returning record data.
        """
        warnings.warn('Use get_mol instead of get_record_mol.', DeprecationWarning)
        if calc3d:
            warnings.warn('calc3d parameter for get_record_mol is no longer supported.', DeprecationWarning)
        return self.get_mol(record_id=csid)


class SearchApi(BaseChemSpider):

    def async_simple_search(self, query):
        """Search ChemSpider with arbitrary query, returning results in order of the best match found.

        This method returns a transaction ID which can be used with other methods to get search status and results.

        Security token is required.

        :param string query: Search query - a name, SMILES, InChI, InChIKey, CSID, etc.
        :returns: Transaction ID.
        :rtype: string
        """
        response = self.request('Search', 'AsyncSimpleSearch', query=query)
        return response.text

    def async_simple_search_ordered(self, query, order=CSID, direction=ASCENDING):
        """Search ChemSpider with arbitrary query, returning results with a custom order.

        This method returns a transaction ID which can be used with other methods to get search status and results.

        Security token is required.

        :param string query: Search query - a name, SMILES, InChI, InChIKey, CSID, etc.
        :param string order: :data:`~chemspipy.api.CSID`, :data:`~chemspipy.api.MASS_DEFECT`,
                             :data:`~chemspipy.api.MOLECULAR_WEIGHT`, :data:`~chemspipy.api.REFERENCE_COUNT`,
                             :data:`~chemspipy.api.DATASOURCE_COUNT`, :data:`~chemspipy.api.PUBMED_COUNT` or
                             :data:`~chemspipy.api.RSC_COUNT`.
        :param string direction: :data:`~chemspipy.api.ASCENDING` or :data:`~chemspipy.api.DESCENDING`.
        :returns: Transaction ID.
        :rtype: string
        """
        response = self.request('Search', 'AsyncSimpleSearchOrdered', query=query, orderBy=ORDERS[order],
                                orderDirection=DIRECTIONS[direction])
        return response.text

    def get_async_search_status(self, rid):
        """Check the status of an asynchronous search operation.

        Security token is required.

        :param string rid: A transaction ID, returned by an asynchronous search method.
        :returns: Unknown, Created, Scheduled, Processing, Suspended, PartialResultReady, ResultReady, Failed,
                  TooManyRecords
        :rtype: string
        """
        response = self.request('Search', 'GetAsyncSearchStatus', rid=rid)
        return response.text

    def get_async_search_status_and_count(self, rid):
        """Check the status of an asynchronous search operation. If ready, a count and message are also returned.

        Security token is required.

        :param string rid: A transaction ID, returned by an asynchronous search method.
        :rtype: dict
        """
        response = self.request('Search', 'GetAsyncSearchStatusAndCount', rid=rid)
        return xml_to_dict(response)

    def get_async_search_result(self, rid):
        """Get the results from a asynchronous search operation. Security token is required.

        :param string rid: A transaction ID, returned by an asynchronous search method.
        :returns: A list of Compounds.
        :rtype: list[:class:`~chemspipy.Compound`]
        """
        warnings.warn('Use get_results instead of get_async_search_result.', DeprecationWarning)
        results = self.get_results(query_id=rid)
        return [Compound(self, record_id) for record_id in results]

    def get_async_search_result_part(self, rid, start=0, count=-1):
        """Get a slice of the results from a asynchronous search operation. Security token is required.

        :param string rid: A transaction ID, returned by an asynchronous search method.
        :param int start: The number of results to skip.
        :param int count: The number of results to return. -1 returns all through to end.
        :returns: A list of Compounds.
        :rtype: list[:class:`~chemspipy.Compound`]
        """
        warnings.warn('Use get_results instead of get_async_search_result_part.', DeprecationWarning)
        if count == -1:
            count = None
        results = self.get_results(query_id=rid, start=start, count=count)
        return [Compound(self, record_id) for record_id in results]

    def get_compound_info(self, csid):
        """Get SMILES, StdInChI and StdInChIKey for a given CSID. Security token is required.

        :param string|int csid: ChemSpider ID.
        :rtype: dict
        """
        warnings.warn('Use get_details instead of get_compound_info.', DeprecationWarning)
        return self.get_details(record_id=csid)

    def get_compound_thumbnail(self, csid):
        """Get PNG image as binary data.

        :param string|int csid: ChemSpider ID.
        :rtype: bytes
        """
        warnings.warn('Use get_image instead of get_compound_thumbnail.', DeprecationWarning)
        return self.get_image(record_id=csid)

    def simple_search(self, query):
        """Search ChemSpider with arbitrary query.

        A maximum of 100 results are returned. Security token is required.

        :param string query: Search query - a name, SMILES, InChI, InChIKey, CSID, etc.
        :returns: List of :class:`Compounds <chemspipy.Compound>`.
        :rtype: list[:class:`~chemspipy.Compound`]
        """
        response = self.request('Search', 'SimpleSearch', query=query)
        return [Compound(self, el.text) for el in response]


class CustomApi(BaseChemSpider):

    def get_compound(self, csid):
        """Return a Compound object for a given ChemSpider ID. Security token is required.

        :param string|int csid: ChemSpider ID.
        :returns: The Compound with the specified ChemSpider ID.
        :rtype: :class:`~chemspipy.Compound`
        """
        return Compound(self, csid)

    def get_compounds(self, csids):
        """Return a list of Compound objects, given a list ChemSpider IDs. Security token is required.

        :param list[string|int] csids: List of ChemSpider IDs.
        :returns: List of Compounds with the specified ChemSpider IDs.
        :rtype: list[:class:`~chemspipy.Compound`]
        """
        return [Compound(self, csid) for csid in csids]

    def search(self, query, order=None, direction=ASCENDING, raise_errors=False):
        """Search ChemSpider for the specified query and return the results. Security token is required.

        :param string|int query: Search query.
        :param string order: (Optional) :data:`~chemspipy.api.CSID`, :data:`~chemspipy.api.MASS_DEFECT`,
                             :data:`~chemspipy.api.MOLECULAR_WEIGHT`, :data:`~chemspipy.api.REFERENCE_COUNT`,
                             :data:`~chemspipy.api.DATASOURCE_COUNT`, :data:`~chemspipy.api.PUBMED_COUNT` or
                             :data:`~chemspipy.api.RSC_COUNT`.
        :param string direction: (Optional) :data:`~chemspipy.api.ASCENDING` or :data:`~chemspipy.api.DESCENDING`.
        :param bool raise_errors: If True, raise exceptions. If False, store on Results ``exception`` property.
        :returns: Search Results list.
        :rtype: Results
        """
        if order and direction:
            return Results(self, self.async_simple_search_ordered, (query, order, direction), raise_errors=raise_errors)
        else:
            return Results(self, self.async_simple_search, (query,), raise_errors=raise_errors)

    # TODO: Wrappers for subscriber role asynchronous searches


class ChemSpider(CustomApi, LookupsApi, RecordsApi, MassSpecApi, SearchApi):
    """Provides access to the ChemSpider API.

    Usage::

        >>> from chemspipy import ChemSpider
        >>> cs = ChemSpider('<YOUR-API-KEY>')

    """

    def __repr__(self):
        return 'ChemSpider()'

# -*- coding: utf-8 -*-
""" Python wrapper for the ChemSpider API.
https://github.com/mcs07/ChemSpiPy

Forked from ChemSpiPy by Cameron Neylon
https://github.com/cameronneylon/ChemSpiPy
"""


import urllib2
from xml.etree import ElementTree as ET


TOKEN  = 'YOU NEED TO INSERT YOUR OWN TOKEN HERE'


class Compound(object):
    """ A class for retrieving record details about a compound by CSID.

    The purpose of this class is to provide access to various parts of the
    ChemSpider API that return information about a compound given its CSID.
    Information is loaded lazily when requested, and cached for future access.
    """

    def __init__(self,csid):
        """ Initialize with a CSID as an int or str """
        if type(csid) is str and csid.isdigit():
            self.csid = csid
        elif type(csid) == int:
            self.csid = str(csid)
        else:
            raise TypeError('Compound must be initialised with a CSID as an int or str')

        self._imageurl = None
        self._mf = None
        self._smiles = None
        self._inchi = None
        self._inchikey = None
        self._averagemass = None
        self._molecularweight = None
        self._monoisotopicmass = None
        self._nominalmass = None
        self._alogp = None
        self._xlogp = None
        self._commonname = None
        self._image = None
        self._mol = None

    def __repr__(self):
        return "Compound(%r)" % self.csid

    @property
    def imageurl(self):
        """ Return the URL of a png image of the 2D structure """
        if self._imageurl is None:
            self._imageurl = 'http://www.chemspider.com/ImagesHandler.ashx?id=%s' % self.csid
        return self._imageurl

    @property
    def mf(self):
        """ Retrieve molecular formula from ChemSpider """
        if self._mf is None:
            self.loadextendedcompoundinfo()
        return self._mf

    @property
    def smiles(self):
        """ Retrieve SMILES string from ChemSpider """
        if self._smiles is None:
            self.loadextendedcompoundinfo()
        return self._smiles

    @property
    def inchi(self):
        """ Retrieve InChi string from ChemSpider """
        if self._inchi is None:
            self.loadextendedcompoundinfo()
        return self._inchi

    @property
    def inchikey(self):
        """ Retrieve InChi string from ChemSpider """
        if self._inchikey is None:
            self.loadextendedcompoundinfo()
        return self._inchikey

    @property
    def averagemass(self):
        """ Retrieve average mass from ChemSpider """
        if self._averagemass is None:
            self.loadextendedcompoundinfo()
        return self._averagemass

    @property
    def molecularweight(self):
        """ Retrieve molecular weight from ChemSpider """
        if self._molecularweight is None:
            self.loadextendedcompoundinfo()
        return self._molecularweight

    @property
    def monoisotopicmass(self):
        """ Retrieve monoisotropic mass from ChemSpider """
        if self._monoisotopicmass is None:
            self.loadextendedcompoundinfo()
        return self._monoisotopicmass

    @property
    def nominalmass(self):
        """ Retrieve nominal mass from ChemSpider """
        if self._nominalmass is None:
            self.loadextendedcompoundinfo()
        return self._nominalmass

    @property
    def alogp(self):
        """ Retrieve ALogP from ChemSpider """
        if self._alogp is None:
            self.loadextendedcompoundinfo()
        return self._alogp

    @property
    def xlogp(self):
        """ Retrieve XLogP from ChemSpider """
        if self._xlogp is None:
            self.loadextendedcompoundinfo()
        return self._xlogp

    @property
    def commonname(self):
        """ Retrieve common name from ChemSpider """
        if self._commonname is None:
            self.loadextendedcompoundinfo()
        return self._commonname

    def loadextendedcompoundinfo(self):
        """ Load extended compound info from the Mass Spec API """
        apiurl = 'http://www.chemspider.com/MassSpecAPI.asmx/GetExtendedCompoundInfo?CSID=%s&token=%s' % (self.csid,TOKEN)
        response = urllib2.urlopen(apiurl)
        tree = ET.parse(response)
        self._mf = tree.find('{http://www.chemspider.com/}MF').text
        self._smiles = tree.find('{http://www.chemspider.com/}SMILES').text
        self._inchi = tree.find('{http://www.chemspider.com/}InChI').text
        self._inchikey = tree.find('{http://www.chemspider.com/}InChIKey').text
        self._averagemass = float(tree.find('{http://www.chemspider.com/}AverageMass').text)
        self._molecularweight = float(tree.find('{http://www.chemspider.com/}MolecularWeight').text)
        self._monoisotopicmass = float(tree.find('{http://www.chemspider.com/}MonoisotopicMass').text)
        self._nominalmass = float(tree.find('{http://www.chemspider.com/}NominalMass').text)
        self._alogp = float(tree.find('{http://www.chemspider.com/}ALogP').text)
        self._xlogp = float(tree.find('{http://www.chemspider.com/}XLogP').text)
        self._commonname = tree.find('{http://www.chemspider.com/}CommonName').text

    @property
    def image(self):
        """ Return string containing PNG binary image data of 2D structure image """
        if self._image is None:
            apiurl = 'http://www.chemspider.com/Search.asmx/GetCompoundThumbnail?id=%s&token=%s' % (self.csid,TOKEN)
            response = urllib2.urlopen(apiurl)
            tree = ET.parse(response)
            self._image = tree.getroot().text
        return self._image

    @property
    def mol(self):
        """ Return record in MOL format """
        if self._mol is None:
            apiurl = 'http://www.chemspider.com/MassSpecAPI.asmx/GetRecordMol?csid=%s&calc3d=true&token=%s' % (self.csid,TOKEN)
            response = urllib2.urlopen(apiurl)
            tree = ET.parse(response)
            self._mol = tree.getroot().text
        return self._mol


def find(query):
    """ Search by Name, SMILES, InChI, InChIKey, etc. Returns first 100 Compounds """
    assert type(query) == str or type(query) == unicode, 'query not a string object'
    searchurl = 'http://www.chemspider.com/Search.asmx/SimpleSearch?query=%s&token=%s' % (urllib2.quote(query), TOKEN)
    response = urllib2.urlopen(searchurl)
    tree = ET.parse(response)
    elem = tree.getroot()
    csid_tags = elem.getiterator('{http://www.chemspider.com/}int')
    compoundlist = []
    for tag in csid_tags:
        compoundlist.append(Compound(tag.text))
    return compoundlist if compoundlist else None


def find_one(query):
    """ Search by Name, SMILES, InChI, InChIKey, etc. Returns a single Compound """
    compoundlist = find(query)
    return compoundlist[0] if compoundlist else None


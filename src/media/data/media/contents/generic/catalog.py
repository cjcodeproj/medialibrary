#!/usr/bin/env python
'''
Module related to the media catalog, which should be universal
across all media types
'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces


class Catalog():
    '''
    The catalog is for identify references to the media, and external
    references pointing to the media
    '''
    def __init__(self, in_chunk):
        self.copyright = None
        if in_chunk is not None:
            self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            if Namespaces.ns_strip(child.tag) == 'copyright':
                self.copyright = Copyright(child)


class Copyright():
    '''Copyright information for the given media'''
    def __init__(self, in_chunk):
        self.year = 0
        self.holders = []
        if in_chunk is not None:
            self._process(in_chunk)

    def _process(self, in_chunk):
        '''Iterate through the elements to map the data to the object'''
        for child in in_chunk:
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'year':
                self.year = int(child.text)
            if ele_name == 'holders':
                self._process_copyright_holders(child)

    def _process_copyright_holders(self, in_chunk):
        for child in in_chunk:
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'holder':
                self.holders.append(child.text)

    def __format__(self, format_spec):
        return f"{self.year}"

#!/usr/bin/env python
'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces

from media.data.media.medium.release import Release, ReleaseException
from media.data.media.medium.productid import ProductId
from media.data.media.medium.productspecs import ProductSpecs


class Medium():
    '''Medium object - the physical thing'''
    def __init__(self, in_element):
        self.release = None
        self.product_id = None
        self.physical_specs = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'release':
                try:
                    self.release = Release(child)
                except ReleaseException as rel:
                    raise MediumException(rel.message) from rel
            if child.tag == Namespaces.nsf('media') + 'productId':
                self.product_id = ProductId(child)
            if child.tag == Namespaces.nsf('media') + 'productSpecs':
                self.product_specs = ProductSpecs(child)


class MediumException(Exception):
    '''
    Exceptions related to the medium object.
    '''
    def __init__(self, in_message):
        super().__init__(in_message)
        self.message = in_message

    def __str__(self):
        return self.message

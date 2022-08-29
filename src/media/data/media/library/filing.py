#!/usr/bin/env python
'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces


class Filing():
    '''
    Data identifying how all instances of this media are
    filed.

    Not done to the invividual instance level, but a more
    generic scope, where all physical copies may be kept in
    a curated collection.
    '''
    def __init__(self, in_element):
        self.catalog = ''
        self.collections = []
        for child in in_element:
            c_tag = Namespaces.ns_strip(child.tag)
            if c_tag == 'catalog':
                self.catalog = child.text
            if c_tag == 'collection':
                self.collections.append(child.text)

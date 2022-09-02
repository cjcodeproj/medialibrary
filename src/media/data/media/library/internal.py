#!/usr/bin/env python
'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces

from media.data.media.library.instances import Instance
from media.data.media.library.filing import Filing


class Library():
    '''Library object - instance tracking and local filing info.'''
    def __init__(self, in_element):
        self.instances = []
        self.filing = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'instances':
                self._pull_instances(child)
            if child.tag == Namespaces.nsf('media') + 'filing':
                self.filing = Filing(child)

    def _pull_instances(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'instance':
                self.instances.append(Instance(child))

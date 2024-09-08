#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

'''
Audio element objects
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801

from media.data.media.contents.generic.catalog import AbstractCatalog
from media.data.nouns import noun_dispatcher
from media.xml.namespaces import Namespaces


class AbstractElement():
    '''
    Root class of all elements
    '''
    def __init__(self):
        self.title = ''
        self.catalog = None

    def _process(self, in_element=None):
        if in_element is not None:
            for child in in_element:
                e_name = Namespaces.ns_strip(child.tag)
                if e_name == 'title':
                    self.title = ElementTitle(child)
                elif e_name == 'catalog':
                    self.catalog = ElementCatalog(child)

    def _extract_catalog_from(self, in_parent):
        if in_parent.catalog is not None:
            self.catalog = ElementCatalog(None)
            if in_parent.catalog.artists is not None:
                self.catalog.artists = in_parent.catalog.artists
            if in_parent.catalog.composers is not None:
                self.catalog.composers = in_parent.catalog.composers


class ElementTitle():
    '''
    Object representation of a song title.
    '''
    def __init__(self, in_element):
        self.main = ''
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'main':
                self.main = child.text

    def __str__(self):
        return self.main


class ElementCatalog(AbstractCatalog):
    '''
    Object representation of a song catalog.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.artists = []
        self.composers = []
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        super()._process(in_element)
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'artists':
                self._process_artists(child)
            elif e_name == 'composers':
                self._process_composers(child)

    def _process_artists(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'artist':
                self.artists.append(noun_dispatcher(child))

    def _process_composers(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'composer':
                self.composers.append(noun_dispatcher(child))


class ElementTechnical():
    '''
    Object representation of a song's technical data.
    '''
    def __init__(self, in_element):
        self.runtime = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        pass

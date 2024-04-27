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
Album Catalog objects
'''

# pylint: disable=too-few-public-methods

from media.data.media.contents.generic.catalog import AbstractCatalog
from media.data.nouns import noun_dispatcher
from media.xml.namespaces import Namespaces


class AlbumCatalog(AbstractCatalog):
    '''
    Subclass for handling catalog data specific
    to a music album.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.artists = []
        self.composers = []
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        super()._process(in_element)
        for child in (in_element):
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'artists':
                self._process_artists(child)

    def _process_artists(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'artist':
                self.artists.append(noun_dispatcher(child))

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
Album objects
'''

# pylint: disable=too-few-public-methods

from media.data.media.contents.internal import AbstractContent
from media.data.media.contents.generic.catalog import Title
from media.data.media.contents.audio.album.catalog import AlbumCatalog
from media.data.media.contents.audio.elements.song import Song
from media.data.media.contents.audio.elements.dialogue import Dialogue
from media.xml.namespaces import Namespaces


class Album(AbstractContent):
    '''
    Album class
    '''
    def __init__(self, in_element):
        super().__init__()
        self.title = ''
        self.catalog = None
        self.elements = []
        self._process(in_element)

    def _process(self, in_element):
        '''
        Processing of top level album elements.
        '''
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'title':
                self.title = Title(child.text)
            elif tagname == 'catalog':
                self.catalog = AlbumCatalog(child)
            elif tagname == 'elements':
                self._load_elements(child)

    def _load_elements(self, in_element):
        '''
        Load element objects and pack them in the elements array.
        '''
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'song':
                self.elements.append(Song(child, self))
            elif tagname == 'dialogue':
                self.elements.append(Dialogue(child, self))

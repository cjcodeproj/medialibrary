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
Album Classification objects
'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces


class AlbumClassification():
    '''
    Subclass for handling catalog data specific
    to a music album.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.genres = None
        self.soundtrack = None
        self.score = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in (in_element):
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'genres':
                self.genres = AlbumClassificationGenres(child)
            elif e_name == 'soundtrack':
                self.soundtrack = AlbumClassificationSoundtrack()
            elif e_name == 'score':
                self.score = AlbumClassificationSoundtrack()


class AlbumClassificationGenres():
    '''
    Album genres.
    '''
    def __init__(self, in_element):
        self.primary = ''
        self.secondary = []
        self.subgenres = []
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'primary':
                self.primary = child.text
            if e_name == 'secondary':
                self.secondary.append(child.text)
            if e_name == 'subgenres':
                self._process_subgenres(child)

    def _process_subgenres(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'subgenre':
                self.subgenres.append(in_element.text)


class AlbumClassificationSoundtrack():
    '''
    Optional element for albums that are soundtracks or scores.
    '''
    def __init__(self):
        self.content = []

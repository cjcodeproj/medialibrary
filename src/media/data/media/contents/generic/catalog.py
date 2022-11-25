#!/usr/bin/env python

#
# Copyright 2022 Chris Josephes
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
Module related to the media catalog, which should be universal
across all media types
'''

# pylint: disable=too-few-public-methods

from media.generic.stringtools import build_filename_string, build_sort_string
from media.xml.namespaces import Namespaces
from media.xml.functions import xs_bool


class Title():
    '''Movie title object'''
    def __init__(self, in_title):
        self.title = in_title.strip()
        if len(self.title) == 0:
            raise TitleValueException("Invalid Title")
        self.sort_title = build_sort_string(self.title)
        self.file_title = build_filename_string(self.title)

    def __hash__(self):
        return hash(self.sort_title)

    def __lt__(self, other):
        return self.sort_title < other.sort_title

    def __gt__(self, other):
        return self.sort_title > other.sort_title

    def __eq__(self, other):
        return self.sort_title == other.sort_title

    def __str__(self):
        return self.title


class TitleValueException(Exception):
    '''Exception raised when a WOA has an invalid title.'''
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class Catalog():
    '''
    The catalog is for identify references to the media, and external
    references pointing to the media
    '''
    def __init__(self, in_chunk):
        self.copyright = None
        self.alt_titles = None
        self.unique_index = None
        if in_chunk is not None:
            self._process(in_chunk)
        if not self.alt_titles:
            self.alt_titles = AlternateTitles(None)

    def _process(self, in_chunk):
        for child in in_chunk:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'copyright':
                self.copyright = Copyright(child)
            if e_name == 'altTitles':
                self.alt_titles = AlternateTitles(child)
            if e_name == 'ucIndex':
                self.unique_index = UniqueConstraints(child)


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


class AlternateTitles():
    '''
    All possible titles that directly reference the work of art
    '''
    def __init__(self, in_chunk):
        self.original_title = ""
        self.variant_title = None
        self.production_title = ""
        self.distribution_title = ""
        self.variant_sort = False
        self.variant_speak = False
        if in_chunk is not None:
            self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'originalTitle':
                self.original_title = child.text
            elif e_name == 'productionTitle':
                self.production_title = child.text
            elif e_name == 'distributiontitle':
                self.distribution_title = child.text
            elif e_name == 'variantTitle':
                self.variant_title = Title(child.text)
                if 'sortable' in child.attrib:
                    self.variant_sort = xs_bool(child.attrib['sortable'])
                if 'textToSpeech' in child.attrib:
                    self.variant_speak = True


class UniqueConstraints():
    '''
    Optional unique identifier.
    '''
    def __init__(self, in_chunk):
        self.index = 0
        self.note = ""
        if in_chunk:
            self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'value':
                self.index = int(child.text)
            elif e_name == 'note':
                self.note = child.text

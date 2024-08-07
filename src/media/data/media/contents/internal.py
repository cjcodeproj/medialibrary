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
Abstract object classes used by all content objects.
'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces
from media.data.media.contents.generic.catalog import (
        Title, TitleValueException, Catalog
        )
from media.generic.titletools import TitleMunger


class AbstractContent():
    '''
    Abstract class for all content, working under the
    assumption that any content object will have a
    title and a catalog.
    '''
    def __init__(self):
        self.title = None
        self.catalog = None
        self.sort_title = ""
        self.unique_key = ""

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'title':
                try:
                    self.title = Title(child.text)
                except TitleValueException as tve:
                    raise ContentException(tve.message) from tve
            if tagname == 'catalog':
                self.catalog = Catalog(child)

    def _post_load_process(self):
        if self.title:
            self._build_unique_key()

    def _build_unique_key(self):
        self.sort_title = TitleMunger.build_sort_cat_title(
                self.title, self.catalog)
        self.unique_key = TitleMunger.build_unique_key_string(
                self.title, self.catalog)

    def catalog_title(self):
        '''
        Return a formatted title that inclues the copyright year.
        '''
        return TitleMunger.build_catalog_title(
                self.title, self.catalog)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
                self.unique_key == other.unique_key


class ContentException(Exception):
    '''
    Root class for all content related exceptions.
    '''
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

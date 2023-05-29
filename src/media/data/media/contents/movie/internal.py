#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
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

'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

from datetime import timedelta
from media.xml.namespaces import Namespaces
from media.data.media.contents.generic.catalog import (
        Title, TitleValueException, Catalog
        )
from media.data.media.contents.generic.story import Story
from media.data.media.contents.genericv.crew import Crew
from media.data.media.contents.genericv.technical import Technical
from media.data.media.contents.movie.classification import Classification
from media.generic.sorting.lists import ContentIndex


class Movie():
    '''Movie object'''
    def __init__(self, in_chunk):
        self.title = None
        self.catalog = None
        self.technical = None
        self.crew = None
        self.sort_title = ""
        self.unique_key = ""
        self._process(in_chunk)

    def build_index_object(self):
        """
        Build an index object to make grouping and
        sorting operations easier.
        """
        return MovieIndexEntry(self)

    def _process(self, in_chunk):
        for child in in_chunk:
            if child.tag == Namespaces.nsf('movie') + 'title':
                try:
                    self.title = Title(child.text)
                except TitleValueException as tve:
                    raise MovieException(tve.message) from tve
            if child.tag == Namespaces.nsf('movie') + 'catalog':
                self.catalog = Catalog(child)
            if child.tag == Namespaces.nsf('movie') + 'classification':
                self.classification = Classification(child)
            if child.tag == Namespaces.nsf('movie') + 'technical':
                self.technical = Technical(child)
            if child.tag == Namespaces.nsf('movie') + 'story':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'description':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'crew':
                self.crew = Crew(child)
        if self.title is not None:
            self._build_unique_key()

    def _build_unique_key(self):
        ukv = None
        cpy = None
        if self.catalog is not None:
            if self.catalog.alt_titles is not None:
                if self.catalog.alt_titles.variant_sort is True:
                    self.sort_title = \
                            self.catalog.alt_titles.variant_title.sort_title
                    self.unique_key = self.sort_title
                else:
                    self.sort_title = self.title.sort_title
                    self.unique_key = self.sort_title
            if self.catalog.copyright is not None:
                cpy = str(self.catalog.copyright.year)
            else:
                cpy = "0000"
            if self.catalog.unique_index is not None:
                ukv = str(self.catalog.unique_index.index)
            else:
                ukv = "1"
            self.unique_key += "-" + cpy + "-" + ukv
        else:
            self.sort_title = self.title.sort_title
            self.unique_key = self.sort_title + "-0000-1"

    def __hash__(self):
        return hash(self.unique_key)

    def __lt__(self, other):
        return self.unique_key < other.unique_key

    def __gt__(self, other):
        return self.unique_key > other.unique_key

    def __eq__(self, other):
        return self.unique_key == other.unique_key


class MovieIndexEntry(ContentIndex):
    '''
    A simple indexing object for movie data.
    '''
    def __init__(self, in_movie):
        super().__init__()
        self.movie = in_movie
        self.year = None
        self.decade = None
        self.primary_g = None
        self.first_letter = None
        self.runtime = None
        self._extract_fields()

    def _extract_fields(self):

        '''
        Extract all the information we need for organizing.
        '''
        if self.movie.catalog:
            cat = self.movie.catalog
            if cat.copyright:
                self.year = cat.copyright.year
                self.decade = int(self.year / 10)
        if self.movie.classification:
            cls = self.movie.classification
            if cls.genres:
                if cls.genres.primary:
                    self.primary_g = cls.genres.primary
        if self.movie.technical:
            tch = self.movie.technical
            if tch.runtime:
                if tch.runtime.overall:
                    self.runtime = tch.runtime.overall
        if not self.runtime:
            self.runtime = timedelta(seconds=0)
        self.sort_title = self.movie.sort_title
        self.first_letter = self.sort_title[0]


class MovieException(Exception):
    '''Exception raised when there is an issue with a movie.'''
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

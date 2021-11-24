#!/usr/bin/env python
'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces
from media.data.media.contents.generic.catalog import Title, Catalog
from media.data.media.contents.genericv.story import Story
from media.data.media.contents.genericv.crew import Crew
from media.data.media.contents.movie.classification import Classification


class Movie():
    '''Movie object'''
    def __init__(self, in_chunk):
        self.title = None
        self.catalog = None
        self.crew = None
        self.unique_key = ""
        self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            if child.tag == Namespaces.nsf('movie') + 'title':
                self.title = Title(child.text)
            if child.tag == Namespaces.nsf('movie') + 'catalog':
                self.catalog = Catalog(child)
            if child.tag == Namespaces.nsf('movie') + 'classification':
                self.classification = Classification(child)
            if child.tag == Namespaces.nsf('movie') + 'story':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'description':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'crew':
                self.crew = Crew(child)
        self._build_unique_key()

    def _build_unique_key(self):
        if self.catalog.alt_titles.variant_sort is True:
            self.unique_key = self.catalog.alt_titles.variant_title.sort_title
        else:
            self.unique_key = self.title.sort_title
        self.unique_key += "-" + str(self.catalog.copyright.year)
        if self.catalog.unique_index is not None:
            self.unique_key += "-" + str(self.catalog.unique_index.index)

    def __hash__(self):
        return hash(self.unique_key)

    def __lt__(self, other):
        return self.unique_key < other.unique_key

    def __gt__(self, other):
        return self.unique_key > other.unique_key

    def __eq__(self, other):
        return self.unique_key == other.unique_key

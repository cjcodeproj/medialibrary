#!/usr/bin/env python
'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces
from media.data.media.contents.generic.catalog import Catalog
from media.data.media.contents.genericv.story import Story
from media.data.media.contents.genericv.crew import Crew


class Movie():
    '''Movie object'''
    def __init__(self, in_chunk):
        self.title = None
        self.catalog = None
        self.crew = None
        self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            if child.tag == Namespaces.nsf('movie') + 'title':
                self.title = Title(child.text)
            if child.tag == Namespaces.nsf('movie') + 'catalog':
                self.catalog = Catalog(child)
            if child.tag == Namespaces.nsf('movie') + 'story':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'description':
                self.story = Story(child)
            if child.tag == Namespaces.nsf('movie') + 'crew':
                self.crew = Crew(child)


class Title():
    '''Movie title object'''
    def __init__(self, in_title):
        self.title = in_title

    def __format__(self, format_spec):
        return format(str(self.title), format_spec)

    def __str__(self):
        return self.title

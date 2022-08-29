#!/usr/bin/env python
'''The main media classes'''

# pylint: disable=too-few-public-methods

from media.generic.stringtools import build_sort_string
from media.xml.namespaces import Namespaces
import media.data.media.library
import media.data.media.medium
import media.data.media.contents.movie


class Media():
    '''Representation of a physical thing that holds content.'''
    def __init__(self, in_chunk):
        self.title = None
        self.library = None
        self.medium = None
        self.contents = []
        self.unique_key = ""
        self._process(in_chunk)

    def _process(self, in_chunk):
        '''Read the passed elemennt and load the interpret the data'''
        for child in in_chunk:
            if child.tag == Namespaces.nsf('media') + 'title':
                self.title = Title(child)
            elif child.tag == Namespaces.nsf('media') + 'library':
                self.library = media.data.media.library.Library(child)
            elif child.tag == Namespaces.nsf('media') + 'medium':
                self.medium = media.data.media.medium.Medium(child)
            elif child.tag == Namespaces.nsf('media') + 'contents':
                self._load_contents(child)
        if self.title is not None:
            self._build_unique_key()

    def _build_unique_key(self):
        self.unique_key = self.title.sort_title

    def _load_contents(self, in_chunk):
        '''Build an array to hold the contents in the media'''
        for element in in_chunk:
            if element.tag == Namespaces.nsf('movie') + 'movie':
                self.contents.append(
                        media.data.media.contents.movie.Movie(element))

    def __str__(self):
        return f"{self.title!s}"


class Title():
    '''Representative of the title of a piece of media'''
    def __init__(self, in_element):
        self.title = None
        self.edition = None
        if in_element is not None:
            self._load_title(in_element)

    def _load_title(self, in_element):
        '''Compose the title based on the passed elements'''
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'main':
                self.title = child.text
            if child.tag == Namespaces.nsf('media') + 'edition':
                self.edition = child.text
        self.sort_title = build_sort_string(self.title)

    def __str__(self):
        '''Return the title of the media'''
        if self.edition:
            return f"{self.title} ({self.edition})"
        return f"{self.title}"

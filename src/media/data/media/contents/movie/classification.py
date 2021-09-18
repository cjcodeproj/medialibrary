#!/usr/bin/env python
'''
Module for movie classification
'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces


class Classification():
    '''
    The classification object records genre information that presents
    a high level overview of the film.
    '''
    def __init__(self, in_chunk):
        self.category = None
        self.genres = None
        if in_chunk is not None:
            self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'category':
                self.category = Category(child)
            elif ele_name == 'genres':
                self.genres = Genres(child)


class Category():
    '''
    A simple breakdown as to whether a film is fiction or non-fiction
    '''
    FICTION = 1
    NONFICTION = 0
    UNKNOWN = -1

    def __init__(self, in_chunk):
        self.value = Category.UNKNOWN
        if in_chunk is not None:
            child = in_chunk[0]
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'fiction':
                self.value = Category.FICTION
            elif ele_name == 'nonfiction':
                self.value = Category.NONFICTION

    def __str__(self):
        '''Return a string representation of the value'''
        s_value = ""
        if self.value == Category.FICTION:
            s_value = "FICTION"
        elif self.value == Category.NONFICTION:
            s_value = "NONFICTION"
        return s_value


class Genres():
    '''
    Genres and subgenres information on a film.
    '''
    def __init__(self, in_chunk):
        self.primary = None
        self.secondary = []
        self.setting = None
        self.specific = None
        self.subgenres = []
        if in_chunk is not None:
            self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'primary':
                self.primary = child.text
            elif ele_name == 'secondary':
                self.secondary.append(child.text)
            elif ele_name == 'setting':
                self.setting = child.text
            elif ele_name == 'specific':
                self.specific = child.text
            elif ele_name == 'subgenres':
                self.subgenres = Genres._process_sg(child)

    @classmethod
    def _process_sg(cls, in_chunk):
        subgenres = []
        for child in in_chunk:
            ele_name = Namespaces.ns_strip(child.tag)
            if ele_name == 'subgenre':
                subgenres.append(child.text)
        return subgenres

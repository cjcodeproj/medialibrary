#!/usr/bin/env python
'''
Module related to the media catalog, which should be universal
across all media types
'''

# pylint: disable=too-few-public-methods

import string
from media.xml.namespaces import Namespaces
from media.xml.functions import xs_bool


class Title():
    '''Movie title object'''
    def __init__(self, in_title):
        self.title = in_title
        self._build_file_title()
        self._build_sort_title()

    def _build_file_title(self):
        level1 = self.title.translate(
                self.title.maketrans("", "", string.punctuation))
        level2 = level1.casefold()
        self.file_title = level2.translate(
                level2.maketrans(" \t\n\r\v", "_____"))

    def _build_sort_title(self):
        level1 = self.title.translate(
                self.title.maketrans("", "", string.punctuation))
        level2 = level1.casefold()
        word_split = level2.split()
        if word_split[0] in ['the', 'a', 'an']:
            article = word_split.pop(0)
            word_split.append(article)
        self.sort_title = "_".join(word_split)

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

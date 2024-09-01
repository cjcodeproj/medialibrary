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
# pylint: disable=too-many-instance-attributes
# pylint: disable=R0801


from datetime import timedelta
from media.data.media.contents.internal import AbstractContent
from media.data.media.contents.generic.catalog import Title
from media.data.media.contents.audio.album.catalog import AlbumCatalog
from media.data.media.contents.audio.album.classification \
    import AlbumClassification
from media.data.media.contents.audio.album.technical \
    import AlbumTechnical
from media.data.media.contents.audio.elements.song import Song
from media.data.media.contents.audio.elements.dialogue import Dialogue
from media.generic.sorting.index import ContentIndex
from media.xml.namespaces import Namespaces


class Album(AbstractContent):
    '''
    Album class
    '''
    def __init__(self, in_element):
        super().__init__()
        self.title = ''
        self.catalog = None
        self.classification = None
        self.technical = None
        self.elements = []
        self.runtime = timedelta(seconds=0)
        self.s_index = None
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
            elif tagname == 'classification':
                self.classification = AlbumClassification(child)
            elif tagname == 'elements':
                self._load_elements(child)
        self._post_load_process()

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

    def _post_load_process(self):
        super()._post_load_process()
        self.technical = AlbumTechnical(self)
        self.s_index = AlbumIndexEntry(self)


class AlbumIndexEntry(ContentIndex):
    '''
    Index object for sorting albums.
    '''
    def __init__(self, in_album):
        super().__init__()
        self.album = in_album
        self.year = None
        self.artists = None
        self.decade = None
        self.primary_g = None
        self.first_letter = None
        self.runtime = None
        self._extract_fields()

    def _extract_fields(self):
        '''
        Extract the title, the artist(s), the copyright year,
        and the genre.  If there's no genre, but there is
        a soundtrack or score element, then create a pseudo-genre
        called Soundtrack or Score respestively.
        '''
        if self.album.catalog:
            cat = self.album.catalog
            if cat.copyright:
                self.year = cat.copyright.year
                self.decade = int(self.year / 10)
            if cat.artists:
                self.artists = AlbumIndexArtists(cat.artists)
        if self.album.classification:
            cls = self.album.classification
            if cls.genres:
                if cls.genres.primary:
                    self.primary_g = cls.genres.primary
            if cls.soundtrack:
                self.primary_g = 'Soundtrack'
            if cls.score:
                self.primary_g = 'Score'
        if not self.artists:
            # It's unlikely we will ever reach this point.
            self.artists = AlbumIndexArtists()
        self.runtime = self.album.technical.runtime
        self.sort_title = self.album.sort_title
        self.first_letter = self.sort_title[0]


class AlbumIndexArtists():
    '''
    An object that works to manage one or more
    artist names with a mechanism for sorting
    and presentation.
    '''
    def __init__(self, in_artists=None):
        self.artists = []
        self.sort_string = ''
        self.formal_string = ''
        if in_artists:
            self.artists = in_artists
            self._build_data()

    def _build_data(self):
        '''
        Build strings suitable for sorting
        the album artists, and also
        presenting the album artists.
        '''
        sort_str = ''
        form_str = ''
        if self.artists:
            for art in self.artists:
                sort_str += art.sort_value + '_'
                form_str += str(art) + ', '
            self.sort_string = sort_str[:-1]
            self.formal_string = form_str[:-2]
        else:
            self.sort_string = 'unknown'
            self.formal_string = 'Unknown'

    def __lt__(self, other):
        return self.sort_string < other.sort_string

    def __rt__(self, other):
        return self.sort_string > other.sort_string

    def __eq__(self, other):
        return self.sort_string == other.sort_string

    def __str__(self):
        return self.formal_string

    def __hash__(self):
        '''
        We need to generate the hash value ourselves.
        '''
        return hash(self.sort_string + self.formal_string)

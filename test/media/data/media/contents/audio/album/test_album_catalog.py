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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.audio.album import Album
from media.data.media.contents.audio.album.catalog import AlbumCatalog
from media.data.nouns import PersonalName


CASE1 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio'>
 <title>Live At The Bar</title>
 <catalog>
  <artists>
   <artist><gn>Wendy</gn><fn>Windings</fn></artist>
  </artists>
 </catalog>
</album>
'''


class TestAlbumCatalogObject(unittest.TestCase):
    '''
    Generic Album Object Tests
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_album_object(self):
        '''
        Assert AlbumCatalog  object is created.
        '''
        self.assertIsInstance(self.album.catalog, AlbumCatalog)


class TestAlbumCatalogArtists(unittest.TestCase):
    '''
    Album Title Tests
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_album_catalog_artists_object(self):
        '''
        Assert album catalog contains one artist object
        '''
        first_artist = self.album.catalog.artists[0]
        self.assertIsInstance(first_artist, PersonalName)

    def test_album_catalog_artist_value(self):
        '''
        Assert artist value is correct.
        '''
        first_artist = self.album.catalog.artists[0]
        self.assertEqual(str(first_artist), 'Wendy Windings')


if __name__ == '__main__':
    unittest.main()

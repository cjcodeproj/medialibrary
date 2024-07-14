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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from datetime import timedelta
from media.data.media.contents.audio.album import Album
from media.data.media.contents.audio.album import AlbumIndexEntry


CASE1 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio'>
 <title>The Road Calls My Name</title>
 <catalog>
  <artists>
   <artist><gn>Bob</gn><fn>McPhereson</fn></artist>
   <artist><grp>The Heavy Haulers</grp></artist>
  </artists>
  <copyright>
   <year>1987</year>
  </copyright>
 </catalog>
 <classification>
  <genres>
   <primary>Country</primary>
  </genres>
 </classification>
 <elements>
  <song id='i01'>
   <title>
    <main>Interstate</main>
   </title>
   <technical>
    <runtime>
     <overall>PT2M</overall>
    </runtime>
   </technical>
  </song>
  <dialogue id='iwb01'>
   <title>
    <main>Interview With Bob</main>
   </title>
   <technical>
    <runtime>
     <overall>PT5M4S</overall>
    </runtime>
   </technical>
  </dialogue>
 </elements>
</album>
'''


class TestAlbumIndexEntryObject(unittest.TestCase):
    '''
    Generic Album Index Entry tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)
        self.album_index = self.album.album_index

    def test_album_index_object(self):
        '''
        Assert index is created.
        '''
        self.assertIsInstance(self.album_index, AlbumIndexEntry)

    def test_ai_sort_title(self):
        '''
        Assert sort title is correct.
        '''
        self.assertEqual(self.album_index.sort_title,
                         'road_calls_my_name_+the')

    def test_ai_first_letter(self):
        '''
        Assert the first letter value is correct.
        '''
        self.assertEqual(self.album_index.first_letter, 'r')

    def test_ai_year(self):
        '''
        Assert year value is correct.
        '''
        self.assertEqual(self.album_index.year, 1987)

    def test_ai_decade(self):
        '''
        Assert the computed decade value is correct.
        '''
        self.assertEqual(self.album_index.decade, 198)

    def test_ai_primary_genre(self):
        '''
        Assert the genre value is correct.
        '''
        self.assertEqual(self.album_index.primary_g, 'Country')

    def test_ai_merge_artists(self):
        '''
        Assert the artist value is correct.
        '''
        self.assertEqual(self.album_index.artists,
                         'mcphereson_bob_heavy_haulers_+the')

    def test_ai_runtime(self):
        '''
        Assert the total runtime is correct.
        '''
        self.assertEqual(self.album_index.runtime,
                         timedelta(seconds=424))


if __name__ == '__main__':
    unittest.main()

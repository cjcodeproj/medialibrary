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
from media.data.media.contents.audio.elements import ElementCatalog
from media.data.media.contents.audio.elements.song import (
        Song, SongTechnical, SongTechnicalRecording, SongTechnicalRuntime
        )
from media.data.nouns import PersonalName


CASE1 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio'>
 <title>Live At The Bar</title>
 <elements>
  <song>
   <title>
    <main>Drinking Alone Tonight</main>
   </title>
   <catalog>
    <artists>
     <artist><gn>Blake</gn><fn>Drake</fn></artist>
    </artists>
    <composers>
     <composer><gn>Chad</gn><fn>Brooks</fn></composer>
    </composers>
   </catalog>
   <technical>
    <studioRecording/>
    <runtime>
     <overall>PT1M20.5S</overall>  <!-- 1 minute, 20 and a half seconds -->
    </runtime>
   </technical>
  </song>
 </elements>
</album>
'''

CASE2 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio'>
 <title>Live At The Bandshell</title>
 <catalog>
  <artists>
   <artist><gn>Francis</gn><fn>Heart</fn></artist>
  </artists>
 </catalog>
 <elements>
  <song>
   <title>
    <main>Drinking Alone Tonight</main>
   </title>
  </song>
 </elements>
</album>
'''


class TestAlbumElementsSongObject(unittest.TestCase):
    '''
    Song object test.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_song_object(self):
        '''
        Assert there is something in elements.
        '''
        song = self.album.elements[0]
        self.assertIsInstance(song, Song)


class TestAlbumElementCatalog(unittest.TestCase):
    '''
    Song catalog tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_song_catalog_object(self):
        '''
        Verify catalog object is set up.
        '''
        song_cat = self.album.elements[0].catalog
        self.assertIsInstance(song_cat, ElementCatalog)

    def test_song_catalog_first_artist_obj(self):
        '''
        Verify object of first artist passed.
        '''
        song_art_one = self.album.elements[0].catalog.artists[0]
        self.assertIsInstance(song_art_one, PersonalName)

    def test_song_catalog_first_artist_val(self):
        '''
        Verify value of first artists passed.
        '''
        song_art_one = self.album.elements[0].catalog.artists[0]
        self.assertEqual(str(song_art_one), 'Blake Drake')

    def test_song_catalog_first_composer_obj(self):
        '''
        Verify object of first composer passed.
        '''
        song_comp_one = self.album.elements[0].catalog.composers[0]
        self.assertIsInstance(song_comp_one, PersonalName)

    def test_song_catalog_first_composer_val(self):
        '''
        Verify value of first composer passed.
        '''
        song_comp_one = self.album.elements[0].catalog.composers[0]
        self.assertEqual(str(song_comp_one), 'Chad Brooks')


class TestAlbumElementInheritedCatalog(unittest.TestCase):
    '''
    Testing catalog entries that are inherited.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE2)
        self.album = Album(xmlroot1)

    def test_song_inherited_catalog_artist(self):
        '''
        Verify the song object has the catalog data from the album.
        '''
        song_art_one = self.album.elements[0].catalog.artists[0]
        self.assertEqual(str(song_art_one), 'Francis Heart')


class TestElementSongTechnical(unittest.TestCase):
    '''
    Song technical tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_technical_obj(self):
        '''
        Confirm the presence of the technical object.
        '''
        technical = self.album.elements[0].technical
        self.assertIsInstance(technical, SongTechnical)


class TestSongTechnicalRecording(unittest.TestCase):
    '''
    Recording type element.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_recording_val(self):
        '''
        Verify the object is set up.
        '''
        record = self.album.elements[0].technical.recording
        self.assertEqual(record, SongTechnicalRecording.STUDIO)

    def test_recording_str_val(self):
        '''
        Verify the value is correct.
        '''
        record = self.album.elements[0].technical.recording
        self.assertEqual(SongTechnicalRecording.to_string(record),
                         'Studio Recording')


class TestAlbumElementSongTechnicalRuntime(unittest.TestCase):
    '''
    Song technical runtime tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.album = Album(xmlroot1)

    def test_runtime_obj(self):
        '''
        Confirm runtime object.
        '''
        runtime = self.album.elements[0].technical.runtime
        self.assertIsInstance(runtime, SongTechnicalRuntime)

    def test_runtime_value(self):
        '''
        Confirm the runtime is properly set.
        '''
        runtime = self.album.elements[0].technical.runtime
        delta_value = timedelta(minutes=1, seconds=20.5)
        self.assertEqual(runtime.overall, delta_value)


if __name__ == '__main__':
    unittest.main()

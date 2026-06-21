#!/usr/bin/env python

#
# Copyright 2026 Chris Josephes
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

'''Unit tests for album unique key class.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.audio.album import Album
from media.data.media.contents.audio.album.unique import AlbumUniqueKey


CASE1 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio/album'>
 <title>Baseball Drama Soundtrack</title>
 <catalog>
  <copyright>
   <year>2013</year>
  </copyright>
  <artists>
   <variousArtists/>
  </artists>
 </catalog>
</album>
'''

UNIQUE_STR1 = 'baseball_drama_soundtrack-2013-138dc3e11c9bf71c'

CASE2 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio/album'>
 <title>Country Roses</title>
 <catalog>
  <copyright>
   <year>1999</year>
  </copyright>
  <artists>
   <artist><gn>Dana Jean</gn><fn>Harley</fn></artist>
   <artist><gn>Phoebe Lynn</gn><fn>Shackelford</fn></artist>
   <artist><gn>Joyce Ann</gn><fn>Smittle</fn></artist>
   <artist><gn>Earline</gn><fn>Oliver</fn></artist>
   <artist><gn>Pam</gn><fn>Smidley</fn></artist>
  </artists>
 </catalog>
</album>
'''

UNIQUE_STR2 = 'country_roses-1999-35e18744fe2d960d'

CASE3 = '''<?xml version='1.0'?>
<album xmlns='http://vectortron.com/xml/media/audio/album'>
 <title>Public Domain Swing Music</title>
 <catalog>
  <artists>
   <artist><grp>The Road Fiddlers</grp></artist>
  </artists>
 </catalog>
</album>
'''

UNIQUE_STR3 = 'public_domain_swing_music-5f2d0d9b8fd7d97e'


class TestFirstAlbumUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for main classification class.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.album = Album(xmlroot)
        self.u_key = self.album.unique_key

    def test_object_class(self):
        '''
        Assert Classification instance is created.
        '''
        self.assertIsInstance(self.u_key, AlbumUniqueKey)

    def test_object_unique_value(self):
        '''
        Assert the hashed value is correct.
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR1)

    def test_full_unique_value(self):
        '''
        Assert the full unique value is correct.
        '''
        self.assertEqual(self.u_key.full(), "album/" + UNIQUE_STR1)


class TestSecondAlbumUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for album test 2.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE2)
        self.album = Album(xmlroot)
        self.u_key = self.album.unique_key

    def test_object_unique_value(self):
        '''
        Test a unique string without a copyright year.
        Test a unique string for an album with multiple artists
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR2)


class TestThirdAlbumUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for album test 3.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE3)
        self.album = Album(xmlroot)
        self.u_key = self.album.unique_key

    def test_object_unique_value(self):
        '''
        Test a unique string without a copyright year.
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR3)


if __name__ == '__main__':
    unittest.main()

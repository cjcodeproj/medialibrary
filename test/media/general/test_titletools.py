#!/usr/bin/env python

#
# Copyright 2025 Chris Josephes
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

'''Unit tests for code handling titles.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.general.titletools import TitleMunger
from media.data.media.contents.movie import Movie


CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>The Awkward Boss</title>
 <catalog>
  <copyright>
   <year>1972</year>
  </copyright>
 </catalog>
</movie>
'''

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>9 Scary Ghosts</title>
 <catalog>
  <altTitles>
   <variantTitle sortable='true'>Nine Scary Ghosts</variantTitle>
  </altTitles>
  <copyright>
   <year>1984</year>
  </copyright>
  <ucIndex>
   <value>2</value>
  </ucIndex>
 </catalog>
</movie>
'''


class TestTitleMunger(unittest.TestCase):
    '''
    Testing the class methods of the TitleMunger object
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)
        self.title = self.movie.title
        self.catalog = self.movie.catalog

    def test_catalog_title(self):
        '''
        Make sure catalog title is correct
        '''
        tm_string = TitleMunger.build_catalog_title(self.title, self.catalog)
        self.assertEqual(tm_string, 'The Awkward Boss (1972)')

    def test_build_filename_string(self):
        '''
        Make sure the code makes a proper filename.
        '''
        tm_file_string = TitleMunger.build_filename_string(self.title)
        self.assertEqual(tm_file_string, 'the_awkward_boss')

    def test_build_sort_string(self):
        '''
        Make sure a sort string is properly made.
        '''
        tm_sort_string = TitleMunger.build_sort_title_string(self.title)
        self.assertEqual(tm_sort_string, 'awkward_boss_+the')

    def test_build_unique_key(self):
        '''
        Make sure the unique key value is correct.
        '''
        tm_key_string = TitleMunger.build_unique_key_string(
                self.title, self.catalog)
        self.assertEqual(tm_key_string, 'awkward_boss_+the-1972-1')

    def test_build_title_path(self):
        '''
        Make sure the title path is correct.
        '''
        tm_path_string = TitleMunger.build_title_path(self.title)
        self.assertEqual(tm_path_string, '/a/aws/')


class TestTitleMungerComplex(unittest.TestCase):
    '''
    More tests of the munger against a more complex title.
    '''

    def setUp(self):
        xmlroot1 = ET.fromstring(CASE2)
        self.movie = Movie(xmlroot1)
        self.title = self.movie.title
        self.catalog = self.movie.catalog

    def test_build_sort_variant_string(self):
        '''
        Get a sort value using the variant string.
        '''
        tm_sort_string = TitleMunger.build_sort_cat_title(
                self.title, self.catalog)
        self.assertEqual(tm_sort_string, 'nine_scary_ghosts')

    def test_build_unique_key_with_index(self):
        '''
        Test a unique key value with a ucIndex value.
        '''
        tm_key_string = TitleMunger.build_unique_key_string(
                self.title, self.catalog)
        self.assertEqual(tm_key_string, 'nine_scary_ghosts-1984-2')


if __name__ == '__main__':
    unittest.main()

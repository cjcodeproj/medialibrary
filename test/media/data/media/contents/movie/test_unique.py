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

'''Unit tests for movie unique key class.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie
from media.data.media.contents.movie.unique import MovieUniqueKey


CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Baseball Drama</title>
 <catalog>
  <copyright>
   <year>2013</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>William</gn><fn>Hill</fn></director>
  </directors>
 </crew>
</movie>
'''

UNIQUE_STR1 = 'baseball_drama-2013-6fcf36f96f284245'

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Mandy &amp; Sandy</title>
 <crew>
  <directors>
   <director><gn>Debra</gn><fn>Lynn</fn></director>
  </directors>
 </crew>
</movie>
'''

UNIQUE_STR2 = 'mandy__sandy-111eaf187972bfb7'

CASE3 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Sudden Romance</title>
</movie>
'''

UNIQUE_STR3 = 'sudden_romance-62f5a66b5496d58e'


class TestFirstMovieUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for main classification class.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot)
        self.u_key = self.movie.unique_key

    def test_object_class(self):
        '''
        Assert Classification instance is created.
        '''
        self.assertIsInstance(self.u_key, MovieUniqueKey)

    def test_object_unique_value(self):
        '''
        Assert the hashed value is correct.
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR1)

    def test_full_unique_value(self):
        '''
        Assert the full unique value is correct.
        '''
        self.assertEqual(self.u_key.full(), "movie/" + UNIQUE_STR1)


class TestSecondMovieUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for movie test 2.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE2)
        self.movie = Movie(xmlroot)
        self.u_key = self.movie.unique_key

    def test_object_unique_value(self):
        '''
        Test a unique string without a copyright year.
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR2)


class TestThirdMovieUniqueKeyCase(unittest.TestCase):
    '''
    Unit tests for movie test 2.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE3)
        self.movie = Movie(xmlroot)
        self.u_key = self.movie.unique_key

    def test_object_unique_value(self):
        '''
        Test a unique string without a copyright year.
        '''
        self.assertEqual(self.u_key.value, UNIQUE_STR3)


if __name__ == '__main__':
    unittest.main()

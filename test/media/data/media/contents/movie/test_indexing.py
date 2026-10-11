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
from media.data.media.contents.movie.indexing import MovieDirPath


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

RESULT1 = 'b/baa/baseball_drama-2013-6fcf36f96f284245'

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Mandy &amp; Sandy</title>
 <catalog>
  <copyright>
   <year>1987</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>Debra</gn><fn>Lynn</fn></director>
  </directors>
 </crew>
</movie>
'''

RESULT2 = 'm/may/mandy_sandy-1987-786f2547d3029f07'

CASE3 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>An Unexpected Sudden Romance</title>
 <catalog>
  <copyright>
   <year>1972</year>
  </copyright>
 </catalog>
</movie>
'''

RESULT3 = 'u/une/an_unexpected_sudden_romance-1972-3398565caf0f6095'

CASE4 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Hunger</title>
 <catalog>
  <copyright>
   <year>1994</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>Steve</gn><fn>Lamont</fn></director>
  </directors>
 </crew>
</movie>
'''

RESULT4 = 'h/hur/hunger-1994-924f877a141b3e95'

CASE5 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>I</title>
 <catalog>
  <copyright>
   <year>2001</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>Manny</gn><fn>Fuller</fn></director>
  </directors>
 </crew>
</movie>
'''

RESULT5 = 'i/i/i-2001-aa306c6386b4d687'

CASE6 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>The Home Becons</title>
 <catalog>
  <copyright>
   <year>1983</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>Tim</gn><fn>McCray</fn></director>
  </directors>
 </crew>
</movie>
'''

RESULT6 = 'h/hos/the_home_becons-1983-86884e86551a3e95'

CASE7 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>The Ex</title>
 <catalog>
  <copyright>
   <year>1995</year>
  </copyright>
 </catalog>
 <crew>
  <directors>
   <director><gn>Michael</gn><fn>Sutherby</fn></director>
  </directors>
 </crew>
</movie>
'''

RESULT7 = 'e/ex/the_ex-1995-0f873eda5794f74b'


class TestMovieDirPathCase(unittest.TestCase):
    '''
    Unit test for MovieDirPath class.
    '''

    def test_movie_path_string(self):
        '''
        Test a regular title string.
        '''
        xmlroot = ET.fromstring(CASE1)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT1)

    def test_movie_path_punct_string(self):
        '''
        Test a title string with punctuation.
        '''
        xmlroot = ET.fromstring(CASE2)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT2)

    def test_movie_path_article_string(self):
        '''
        Test a title string with a leading article.
        '''
        xmlroot = ET.fromstring(CASE3)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT3)

    def test_movie_path_single_word_string(self):
        '''
        Test a title with a single word.
        '''
        xmlroot = ET.fromstring(CASE4)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT4)

    def test_movie_path_single_letter_string(self):
        '''
        Test a title with a single letter.
        '''
        xmlroot = ET.fromstring(CASE5)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT5)

    def test_movie_path_the_article_string(self):
        '''
        Test a title with a 'the' article.
        '''
        xmlroot = ET.fromstring(CASE6)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT6)

    def test_movie_path_article_short_title_string(self):
        '''
        Test a title with a 'the' article, and a short word.
        '''
        xmlroot = ET.fromstring(CASE7)
        movie = Movie(xmlroot)
        path = MovieDirPath.build_path(movie)
        self.assertEqual(path, RESULT7)


if __name__ == '__main__':
    unittest.main()

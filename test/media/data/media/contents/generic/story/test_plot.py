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

'''Unit tests for plot  class.'''

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie
from media.data.media.contents.generic.story import Plot

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Where's The Ardvark?</title>
 <story>
  <plot>
   A lone dolphin tries to reunite with his trainer after
   being accidentally abandoned at sea.
  </plot>
 </story>
</movie>
'''

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Where's The Ardvark?</title>
 <story>
  <plot>
   <chr>Samantha</chr> must piece together the clues as to why her
   entire family (except her) was kidnapped.
  </plot>
 </story>
</movie>
'''


class TestPlot(unittest.TestCase):
    '''
    Tests against Plot class (generic story plot).
    '''
    def setUp(self):
        '''
        Set up movie object.
        '''
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_plot_object(self):
        '''
        Assert Plot instance is created.
        '''
        plot = self.movie.story.plot
        self.assertIsInstance(plot, Plot)

    def test_plot_string_value(self):
        '''
        Assert plot string value can be retrieved.
        '''
        plot = self.movie.story.plot
        str1 = "A lone dolphin tries to reunite with his trainer " + \
               "after being accidentally abandoned at sea."
        self.assertEqual(str(plot), str1)

    def test_plot_no_trailing_whitespace(self):
        '''
        Assert plot string has no trailing whitespace.
        '''
        plot = self.movie.story.plot
        p_strip = str(plot).rstrip()
        self.assertEqual(str(plot), p_strip)


if __name__ == '__main__':
    unittest.main()

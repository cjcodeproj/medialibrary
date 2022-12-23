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
from media.data.media.contents.movie import Movie
from media.data.media.contents.genericv.crew import (
        Crew, Cast, Role, CharacterName
        )

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>A River Turns Inward</title>
 <crew>
  <cast>
   <role>
    <actor><gn>Marty</gn><fn>Goofus</fn></actor>
    <as><prefix>Judge</prefix><gn>Bettle</gn><fn>Gallant</fn>
     <suffix tpe='generational'>Sr.</suffix><aspect>voice</aspect></as>
   </role>
  </cast>
 </crew>
</movie>
'''


class TestCrewObjects(unittest.TestCase):
    '''
    Test for crew level classes.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_crew_class_instance(self):
        '''
        Verify crew object is created.
        '''
        self.assertIsInstance(self.movie.crew, Crew)

    def test_cast_instance(self):
        '''
        Verify cast object is created.
        '''
        self.assertIsInstance(self.movie.crew.cast, Cast)

    def test_first_role_instance(self):
        '''
        Verify a role object is created.
        '''
        self.assertIsInstance(self.movie.crew.cast.cast[0], Role)

    def test_first_role_instance_portrays_character(self):
        '''
        Verify role object contains a CharacterName object.
        '''
        self.assertIsInstance(self.movie.crew.cast.cast[0].portrays[0],
                              CharacterName)


class TestCastRoleAs(unittest.TestCase):
    '''
    CharacterName class tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_character_given_name(self):
        '''
        Test creation of CharacterName object.
        '''
        cn1 = self.movie.crew.cast.cast[0].portrays[0]
        self.assertEqual(cn1.chunk['given'], "Bettle")

    def test_character_aspect(self):
        '''
        Test aspect value of character name.
        '''
        cn1 = self.movie.crew.cast.cast[0].portrays[0]
        self.assertEqual(cn1.aspect, 'voice')


if __name__ == '__main__':
    unittest.main()

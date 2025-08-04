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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from datetime import timedelta
from media.data.media.contents.movie import Movie
from media.data.media.contents.genericv.technical import Runtime, Technical
from media.data.media.contents.genericv.variants import (
        OriginalVariant, Variant, VariantPool)

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Superfast Supercars</title>
 <variants>
  <original id='orig'/>
  <variant id='unrated'>
   <name>Unrated Edition</name>
   <notes>More gore</notes>
   <technical>
    <runtime>
     <overall>PT2H12M05S</overall>
    </runtime>
   </technical>
  </variant>
 </variants>
</movie>
'''

CASE2 = '''<?xml version='1.0'?>
<variants xmlns='http://vectortron.com/xml/media/movie'>
 <original id='orig'/>
 <variant id='director'>
  <name>Director's Cut</name>
  <notes>More drama</notes>
 </variant>
 <variant id='unrated'>
  <name>Home video release</name>
 </variant>
</variants>
'''


class TestVariantPool(unittest.TestCase):
    '''
    Test VariantPool functions.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE2)
        self.variant_list = VariantPool.read_variants(xmlroot1)

    def test_parsed_variant_count(self):
        '''
        Verify parsing function reads variants correctly.
        '''
        self.assertEqual(len(self.variant_list), 3)


class TestVariantObjects(unittest.TestCase):
    '''
    Tests for Variant classes.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_variant_array(self):
        '''
        Verify variants array has 2 objects.
        '''
        self.assertEqual(len(self.movie.variants), 2)

    def test_original_instance(self):
        '''
        Verify class of first object.
        '''
        self.assertIsInstance(self.movie.variants[0], OriginalVariant)

    def test_variant_instance(self):
        '''
        Verify class of second object.
        '''
        self.assertIsInstance(self.movie.variants[1], Variant)


class TestVariantData(unittest.TestCase):
    '''
    Tests for Variant objects.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.variants = Movie(xmlroot1).variants

    def test_variant_id(self):
        '''
        Test the variant id value.
        '''
        self.assertEqual(self.variants[0].id, 'orig')

    def test_variant_name(self):
        '''
        Verify the name is set correctly.
        '''
        self.assertEqual(self.variants[1].name, 'Unrated Edition')

    def test_variant_notes(self):
        '''
        Test the note value of the variant.
        '''
        self.assertEqual(self.variants[1].notes, 'More gore')

    def test_variant_technical_object(self):
        '''
        Test the technical object the second variant should contain.
        '''
        self.assertIsInstance(self.variants[1].technical, Technical)

    def test_variant_tech_runtime_object(self):
        '''
        Test the runtime object the second variant should contain.
        '''
        self.assertIsInstance(self.variants[1].technical.runtime, Runtime)

    def test_variant_runtime_value(self):
        '''
        Test the runtime value of the second variant.
        '''
        t_delta = timedelta(hours=2, minutes=12, seconds=5)
        self.assertEqual(self.variants[1].technical.runtime.overall, t_delta)


if __name__ == '__main__':
    unittest.main()

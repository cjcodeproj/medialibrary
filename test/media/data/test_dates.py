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

'''
Unit tests against date objects.
'''

import unittest
import xml.etree.ElementTree as ET
from media.data.dates import ExactDate, RangeDate
from media.xml.namespaces import Namespaces

CASE1 = '''<?xml version='1.0'?>
<date xmlns='http://vectortron.com/xml/media/media'>
<exact>2020-10-30</exact></date>
'''

CASE2 = '''<?xml version='1.0'?>
<date xmlns='http://vectortron.com/xml/media/media'>
<from>2020-10-30</from><range>P3Y</range></date>
'''


class TestExactDate(unittest.TestCase):
    '''
    Test suite for the ExactDate object.
    '''
    def setUp(self):
        '''
        Test initialization.
        '''
        xmlroot = ET.fromstring(CASE1)
        date_element = xmlroot.findall('./media:exact', Namespaces.ns)[0]
        self.ed_object = ExactDate(date_element)

    def test_ed_object_initialization(self):
        '''
        Make sure date object is created.
        '''
        self.assertIsInstance(self.ed_object, ExactDate)

    def test_ed_object_value(self):
        '''
        Make sure the date is set correctly.
        '''
        self.assertEqual(str(self.ed_object), '2020-10-30')


class TestRangeDate(unittest.TestCase):
    '''
    First test suite for the RangeDate object.
    '''
    def setUp(self):
        '''
        Test initialization.
        '''
        xmlroot = ET.fromstring(CASE2)
        start_element = xmlroot.findall('./media:from', Namespaces.ns)[0]
        range_element = xmlroot.findall('./media:range', Namespaces.ns)[0]
        self.rd_object = RangeDate(start_element, range_element)

    def test_rd_object_initialization(self):
        '''
        Make sure date object is created.
        '''
        self.assertIsInstance(self.rd_object, RangeDate)

    def test_rd_object_from_date(self):
        '''
        Confirm start date is set.
        '''
        self.assertEqual(self.rd_object.date, '2020-10-30')

    def test_rd_object_range_interval(self):
        '''
        Confirm range interval is set.
        '''
        self.assertEqual(self.rd_object.end, 'P3Y')

    def test_rd_object_full_string(self):
        '''
        Confirm full text string.
        '''
        self.assertEqual(str(self.rd_object), '2020-10-30 -> P3Y')


if __name__ == '__main__':
    unittest.main()

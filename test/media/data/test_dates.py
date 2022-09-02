#!/usr/bin/env python
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

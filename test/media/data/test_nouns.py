#!/usr/bin/env python
"""Unit tests against proper noun objects.
"""

import unittest
import xml.etree.ElementTree as ET
from media.data.nouns import Name

CASE1 = '''<?xml version='1.0'?>
<name xmlns='http://vectortron.com/xml/media/movie'>
 <gn>Patrick</gn><fn>Swayze</fn>
</name>
'''

CASE2 = '''<?xml version='1.0'?>
<name xmlns='http://vectortron.com/xml/media/movie'>
 <gn>Barbara</gn><fn>Stanwick</fn>
</name>
'''

CASE3 = '''<?xml version='1.0'?>
<name xmlns='http://vectortron.com/xml/media/movie'>
 <gn>Jack</gn>
</name>
'''


class TestProperNounName(unittest.TestCase):
    """Test suite for Name (set 1)
    """
    def setUp(self):
        """Test initialization."""
        xmlroot = ET.fromstring(CASE1)
        self.name = Name(xmlroot)

    def test_name_member(self):
        """Assert name instance is created."""
        self.assertIsInstance(self.name, Name)

    def test_name_value(self):
        """Assert name returns proper string."""
        self.assertEqual(str(self.name), 'Patrick Swayze')


class TestProperNounNameSorting(unittest.TestCase):
    """Test suite for Name sorting.
    """
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        xmlroot2 = ET.fromstring(CASE2)
        xmlroot3 = ET.fromstring(CASE3)
        self.name1 = Name(xmlroot1)
        self.name2 = Name(xmlroot2)
        self.name3 = Name(xmlroot3)

    def test_regular_name_sort(self):
        """Compare sorting of two regular names.
        """
        self.assertTrue(self.name1 > self.name2)

    def test_special_name_sort(self):
        """Compare sort between full name and given name.
        """
        self.assertTrue(self.name3 < self.name1)

    def test_special_name_sort_value(self):
        """Verify sort_value value."""
        self.assertEqual(self.name3.sort_value, 'jack')

    def test_name_sort_value(self):
        """Verify sort value for regular name."""
        self.assertEqual(self.name1.sort_value, 'swayze_patrick')

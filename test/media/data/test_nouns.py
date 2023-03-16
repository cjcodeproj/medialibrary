#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
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

"""Unit tests against proper noun objects.
"""

import unittest
import xml.etree.ElementTree as ET
from media.data.nouns import Noun, PersonalName, noun_dispatcher

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

CASE4 = '''<?xml version='1.0'?>
<name xmlns='http://vectortron.com/xml/media/movie'>
 <pcn>Sasha X</pcn>
</name>
'''

CASE5 = '''<?xml version='1.0'?>
<name xmlns='http://vectortron.com/xml/media/movie'>
 <pgn>Alicia</pgn><gn>Susan</gn><fn>Swayze</fn>
</name>
'''

CASE6 = '''<?xml version='1.0'?>
<music xmlns='http://vectortron.com/xml/media/movie'>
 <grp>Rolling Boulders</grp>
</music>
'''


class TestProperNounName(unittest.TestCase):
    """Test suite for PersonalName (set 1)
    """
    def setUp(self):
        """Test initialization."""
        xmlroot = ET.fromstring(CASE1)
        self.name = PersonalName(xmlroot)

    def test_name_member(self):
        """Assert name instance is created."""
        self.assertIsInstance(self.name, PersonalName)

    def test_name_value(self):
        """Assert name returns proper string."""
        self.assertEqual(str(self.name), 'Patrick Swayze')


class TestProperNounPersonalNameSorting(unittest.TestCase):
    """Test suite for PersonalName sorting.
    """
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        xmlroot2 = ET.fromstring(CASE2)
        xmlroot3 = ET.fromstring(CASE3)
        xmlroot4 = ET.fromstring(CASE4)
        xmlroot5 = ET.fromstring(CASE5)
        self.name1 = PersonalName(xmlroot1)
        self.name2 = PersonalName(xmlroot2)
        self.name3 = PersonalName(xmlroot3)
        self.name4 = PersonalName(xmlroot4)
        self.name5 = PersonalName(xmlroot5)

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

    def test_given_personal_name_sort_value(self):
        """Verify given name vs. preferred given name."""
        self.assertTrue(self.name5 < self.name1)

    def test_complete_name_sort_value(self):
        """Verify a complete name sort value is correct."""
        self.assertEqual(self.name4.sort_value, 'sasha_x')

    def test_preferred_vs_given_sort(self):
        """Verify that sorting works with a pgn element."""
        self.assertTrue(self.name5 < self.name1)


class TestNounDispatchFunction(unittest.TestCase):
    """Test suite for noun_dispatcher function.
    """
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE6)
        self.grp1 = noun_dispatcher(xmlroot1)

    def test_noun_dispatcher_group(self):
        """Verify dispatcher preserves correct value."""
        self.assertEqual(str(self.grp1), 'Rolling Boulders')

    def test_noun_dispatcher_class(self):
        """Verify dispatcher sends correct object class."""
        self.assertIsInstance(self.grp1, Noun)

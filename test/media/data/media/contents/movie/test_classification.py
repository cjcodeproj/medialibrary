#!/usr/bin/env python
'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie.classification import (
        Classification, Category, Genres
        )

CASE1 = '''<?xml version='1.0'?>
<classification xmlns='http://vectortron.com/xml/media/movie'>
 <category><fiction/></category>
 <genres>
  <primary>Comedy</primary>
  <secondary>Mystery</secondary>
  <subgenres>
   <subgenre>based on a book</subgenre>
  </subgenres>
 </genres>
</classification>
'''


class TestClassification(unittest.TestCase):
    '''
    Unit tests for main classification class.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.classification = Classification(xmlroot)

    def test_classification_member(self):
        '''
        Assert Classification instance is created.
        '''
        self.assertIsInstance(self.classification, Classification)

    def test_category_member(self):
        '''
        Assert Category instance is created.
        '''
        self.assertIsInstance(self.classification.category, Category)

    def test_genres_member(self):
        '''
        Assert Genres instance is created.
        '''
        self.assertIsInstance(self.classification.genres, Genres)


class TestCategory(unittest.TestCase):
    '''
    Tests related to Category object.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.classification = Classification(xmlroot)

    def test_category(self):
        '''
        Assert Category value returns proper string.
        '''
        self.assertEqual(str(self.classification.category), 'FICTION')


class TestGenres(unittest.TestCase):
    '''
    Tests related to Genre object.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.classification = Classification(xmlroot)

    def test_primary_genre(self):
        '''
        Test that the primary classification has been set.
        '''
        self.assertEqual(self.classification.genres.primary, "Comedy")

    def test_secondary_genre1(self):
        '''
        Assert that the secondary classification has been set.
        '''
        self.assertIn('Mystery', self.classification.genres.secondary)

    def test_subgenre_set(self):
        '''
        Assert subgenre value is properly set.
        '''
        self.assertIn('based on a book', self.classification.genres.subgenres)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
'''Unit tests for keywords classes.'''

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie
from media.data.media.contents.generic.keywords import (
        Keywords, GenericKeyword, ProperNounKeyword
        )

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Where's The Ardvark?</title>
 <story>
  <keywords>
   <generic>bank robbery</generic>
   <generic>hotel</generic>
   <properNoun><place><ci>Miami</ci><st>Florida</st></place></properNoun>
   <properNoun><entity>US Army</entity></properNoun>
  </keywords>
 </story>
</movie>
'''


class TestKeywords(unittest.TestCase):
    '''
    Tests against Keywords class.
    '''
    def setUp(self):
        '''
        Test Keywords object.
        '''
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_keywords_object(self):
        '''
        Assert Keywords instance is created.
        '''
        kws = self.movie.story.keywords
        self.assertIsInstance(kws, Keywords)

    def test_keywords_contains_group(self):
        '''
        Assert generic group is in Keywords instance.
        '''
        kws = self.movie.story.keywords
        self.assertIn('generic', kws.pool_list())


class TestGenericKeyword(unittest.TestCase):
    '''
    Tests against GenericKeyword class.
    '''
    def setUp(self):
        '''
        Test Setup Method
        '''
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_generic_object(self):
        '''
        Assert GenericKeyword instance is created
        '''
        keyword = self.movie.story.keywords.pools['generic'][0]
        self.assertIsInstance(keyword, GenericKeyword)

    def test_generic_set(self):
        '''
        Assert GenericKeyword has a value
        '''
        keyword = self.movie.story.keywords.pools['generic'][0]
        self.assertEqual(str(keyword), 'bank robbery')

    def test_generic_sort_value(self):
        '''
        Assert sort_value is properly set.
        '''
        keyword = self.movie.story.keywords.pools['generic'][0]
        self.assertEqual(keyword.sort_value, 'bank robbery')

    def test_generic_object_order(self):
        '''
        Assert 2 GenericKeywords can be sort compared
        '''
        keyword1 = self.movie.story.keywords.pools['generic'][0]
        keyword2 = self.movie.story.keywords.pools['generic'][1]
        self.assertTrue(keyword1 < keyword2)

    def test_generic_object_detail(self):
        '''
        Assert GenericKeyword detail value properly set.
        '''
        keyword = self.movie.story.keywords.pools['generic'][0]
        self.assertEqual(keyword.detail(), 'generic/bank robbery')


class TestProperNounKeyword(unittest.TestCase):
    '''
    Tests against ProperNounKeyword class.
    '''
    def setUp(self):
        '''
        Test Setup Method
        '''
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_propernoun_object(self):
        '''
        Assert ProperNounKeyword instance is created
        '''
        keyword = self.movie.story.keywords.pools['generic'][2]
        self.assertIsInstance(keyword, ProperNounKeyword)

    def test_propernoun_object_set(self):
        '''
        Assert ProperNounKeyword has a value.
        '''
        keyword = self.movie.story.keywords.pools['generic'][2]
        self.assertEqual(str(keyword), 'Miami (Florida)')

    def test_propernoun_sort_value(self):
        '''
        Assert sort_value is properly set.
        '''
        keyword = self.movie.story.keywords.pools['generic'][2]
        self.assertTrue(keyword.sort_value, 'miami')

    def test_propernoun_object_order(self):
        '''
        Assert ProperNounKeyword can be sort compared.
        '''
        keyword1 = self.movie.story.keywords.pools['generic'][2]
        keyword2 = self.movie.story.keywords.pools['generic'][1]
        self.assertTrue(keyword2 < keyword1)

    def test_propernoun_object_detail(self):
        '''
        Assert ProperNounKeyword detail value.
        '''
        keyword = self.movie.story.keywords.pools['generic'][2]
        self.assertEqual(keyword.detail(), 'properNoun/place/Miami (Florida)')

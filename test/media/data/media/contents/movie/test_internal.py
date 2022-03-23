#!/usr/bin/env python
'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie, MovieException

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>A River Turns Inward</title>
</movie>
'''

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Love And Crime In Sacramento</title>
</movie>
'''

CASE3 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Valerie's Mistake, Greg's Terror</title>
 <catalog>
  <copyright>
   <year>1994</year>
  </copyright>
 </catalog>
</movie>
'''

CASE4 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>74 Minutes To Countdown</title>
 <catalog>
  <altTitles>
   <variantTitle
    sortable='true'>Seventy Four Minutes To Countdown</variantTitle>
  </altTitles>
  <copyright>
   <year>1977</year>
  </copyright>
  <ucIndex>
   <value>2</value>
  </ucIndex>
 </catalog>
</movie>
'''

CASE5 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title> </title>
 <catalog>
  <copyright>
   <year>1977</year>
  </copyright>
 </catalog>
</movie>
'''


class TestMovie(unittest.TestCase):
    '''
    Basic movie object tests.
    '''
    def setUp(self):
        '''
        Setup Test Method.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot)

    def test_movie_instance(self):
        '''
        Assert the movie instance is created.
        '''
        self.assertIsInstance(self.movie, Movie)

    def test_movie_unique_key(self):
        '''
        Assert the unique key value for a given movie.
        '''
        self.assertEqual(self.movie.unique_key,
                         "river_turns_inward__a-0000-1")


class TestMovieSort(unittest.TestCase):
    '''
    Test for multi-movie object sorting.
    '''
    def setUp(self):
        '''
        Setup Test Method.
        '''
        xmlroot1 = ET.fromstring(CASE1)
        xmlroot2 = ET.fromstring(CASE2)
        self.movie1 = Movie(xmlroot1)
        self.movie2 = Movie(xmlroot2)

    def test_movie_object_order(self):
        '''
        Assert the sorting functionality between two Movie objects.
        '''
        self.assertTrue(self.movie2 < self.movie1)


class TestMoviePunctuationTitle(unittest.TestCase):
    '''
    Punctuation title movie tests.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE3)
        self.movie = Movie(xmlroot1)

    def test_movie_punctuation_unique_key(self):
        '''
        Assert unique_key removes punctuation.
        '''
        self.assertEqual(self.movie.unique_key,
                         "valeries_mistake_gregs_terror-1994-1")


class TestMovieVariantTitle(unittest.TestCase):
    '''Variant title movie tests.'''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE4)
        xmlroot2 = ET.fromstring(CASE2)
        self.movie1 = Movie(xmlroot1)
        self.movie2 = Movie(xmlroot2)

    def test_movie_variant_unique_key(self):
        '''
        Assert unique_key against a movie with a variant title.
        '''
        self.assertEqual(self.movie1.unique_key,
                         "seventy_four_minutes_to_countdown-1977-2")

    def test_movie_variant_order(self):
        '''
        Assert sort order between two movies.
        '''
        self.assertTrue(self.movie1 > self.movie2)


class TestMovieTitleException(unittest.TestCase):
    '''Movie title exception'''
    def test_title_exception(self):
        '''Text exception with title triggers Movie object exception.'''
        xmlroot1 = ET.fromstring(CASE5)
        with self.assertRaises(MovieException):
            movie1 = Movie(xmlroot1)
            del movie1

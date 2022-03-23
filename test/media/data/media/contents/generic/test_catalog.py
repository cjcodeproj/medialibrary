#!/usr/bin/env python
'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie
from media.data.media.contents.generic.catalog import (
        Title, TitleValueException, Catalog, Copyright, AlternateTitles,
        UniqueConstraints
        )
from media.xml.namespaces import Namespaces

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>A River Turns Inward</title>
</movie>
'''

CASE2 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>Love And Crime In Sacramento</title>
 <catalog>
  <altTitles>
   <originalTitle>Love And Crime In Bakersfield</originalTitle>
  </altTitles>
  <copyright>
   <year>1972</year>
   <holders>
    <holder>A Can Apart Productions, LLC</holder>
   </holders>
  </copyright>
  <ucIndex>
   <value>2</value>
   <note>Big Movie Year</note>
  </ucIndex>
 </catalog>
</movie>
'''

CASE3 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>74 Minutes To Countdown</title>
 <catalog>
  <altTitles>
   <variantTitle
   sortable='true'>Seventy Four Minutes To Countdown</variantTitle>
  </altTitles>
  <copyright>
   <year>1977</year>
   <holders>
    <holder>Sit, Ubuntu, Sit</holder>
   </holders>
  </copyright>
 </catalog>
</movie>
'''

CASE4 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title> </title>
 <catalog>
  <copyright>
   <year>1977</year>
  </copyright>
 </catalog>
</movie>
'''

CASE5 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>The Stranger</title>
 <catalog>
  <copyright>
   <year>1978</year>
  </copyright>
 </catalog>
</movie>
'''

CASE6 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>The Stranger Comes Back</title>
 <catalog>
  <copyright>
   <year>1979</year>
  </copyright>
 </catalog>
</movie>
'''


class TestTitle(unittest.TestCase):
    '''
    Generic Title Object
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE1)
        self.movie = Movie(xmlroot1)

    def test_title_object(self):
        '''
        Assert Title instance is created.
        '''
        self.assertIsInstance(self.movie.title, Title)

    def test_title_set(self):
        '''
        Assert Title instance has correct value.
        '''
        self.assertEqual(str(self.movie.title), "A River Turns Inward")

    def test_title_sort_title(self):
        '''
        Assert Title instance has correct sort_value.
        '''
        self.assertEqual(self.movie.title.sort_title, "river_turns_inward__a")

    def test_title_file_title(self):
        '''
        Assert Title instance has correct file_title.
        '''
        self.assertEqual(self.movie.title.file_title, "a_river_turns_inward")


class TestTitleIndependent(unittest.TestCase):
    '''
    Test Title objects independtly of movie objects.
    '''
    def test_empty_title(self):
        '''
        Assert an empty title string will fail.
        '''
        xmlroot = ET.fromstring(CASE4)
        title_element = xmlroot.findall('./movie:title', Namespaces.ns)[0]
        with self.assertRaises(TitleValueException):
            title_object = Title(title_element.text)
            del title_object

    def test_populated_title(self):
        '''
        Assert a populated title string will succeed.
        '''
        xmlroot = ET.fromstring(CASE3)
        title_element = xmlroot.findall('./movie:title', Namespaces.ns)[0]
        title_object = title_element.text
        self.assertEqual(str(title_object), "74 Minutes To Countdown")


class TestTitleSorting(unittest.TestCase):
    '''
    Test title object sorting when an article is in the title.
    '''
    def setUp(self):
        xmlroot1 = ET.fromstring(CASE5)
        xmlroot2 = ET.fromstring(CASE6)
        self.movie1 = Movie(xmlroot1)
        self.movie2 = Movie(xmlroot2)

    def test_title_with_article_comparision(self):
        '''
        Make sure articles do not interfere with title sorting.
        '''
        self.assertTrue(self.movie1.title < self.movie2.title)


class TestCatalog(unittest.TestCase):
    '''
    Tests Catalog object.
    '''
    def setUp(self):
        '''
        Test Setup Method.
        '''
        xmlroot1 = ET.fromstring(CASE2)
        self.movie = Movie(xmlroot1)

    def test_catalog_object(self):
        '''
        Assert Catalog instance is created.
        '''
        self.assertIsInstance(self.movie.catalog, Catalog)

    def test_alt_title_object(self):
        '''
        Assert AlternateTitles instance is created.
        '''
        self.assertIsInstance(self.movie.catalog.alt_titles, AlternateTitles)

    def test_copyright_object(self):
        '''
        Assert Copyright instance is created.
        '''
        self.assertIsInstance(self.movie.catalog.copyright, Copyright)

    def test_unique_constraints_object(self):
        '''
        Assert UniqueConstraints instace is created.
        '''
        self.assertIsInstance(self.movie.catalog.unique_index,
                              UniqueConstraints)


class TestCopyright(unittest.TestCase):
    '''
    Test Copyright object.
    '''
    def setUp(self):
        '''
        Test Setup Method.
        '''
        xmlroot1 = ET.fromstring(CASE2)
        self.movie = Movie(xmlroot1)

    def test_copyright_year(self):
        '''
        Assert Copyright instance has correct year value.
        '''
        self.assertEqual(self.movie.catalog.copyright.year, 1972)

    def test_copyright_holders(self):
        '''
        Assert Copyright instance has correct holder value.
        '''
        self.assertIn("A Can Apart Productions, LLC",
                      self.movie.catalog.copyright.holders)


class TestAlternateTitles(unittest.TestCase):
    '''
    Test AlternateTitles object.
    '''
    def setUp(self):
        '''
        Test Setup Method.
        '''
        xmlroot1 = ET.fromstring(CASE2)
        xmlroot2 = ET.fromstring(CASE3)
        self.catalog1 = Movie(xmlroot1).catalog
        self.catalog2 = Movie(xmlroot2).catalog

    def test_variant_title(self):
        '''
        Assert AlternateTitle/variant_title is properly set.
        '''
        self.assertEqual(str(self.catalog2.alt_titles.variant_title),
                         "Seventy Four Minutes To Countdown")

    def test_original_title(self):
        '''
        Assert AlternateTitle/original_title is properly set.
        '''
        self.assertEqual(self.catalog1.alt_titles.original_title,
                         "Love And Crime In Bakersfield")


class TestUniqueConstraints(unittest.TestCase):
    '''
    Test UniqueConstraints object.
    '''
    def setUp(self):
        '''
        Test Setup Method.
        '''
        xmlroot1 = ET.fromstring(CASE2)
        self.catalog1 = Movie(xmlroot1).catalog

    def test_unique_constraint_index(self):
        '''
        Test UniqueConstraint/index value is properly set.
        '''
        self.assertEqual(self.catalog1.unique_index.index, 2)

    def test_unique_constraint_note(self):
        '''
        Assert UniqueConstraint/note value is properly set.
        '''
        self.assertEqual(self.catalog1.unique_index.note, "Big Movie Year")


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET

from media.data.media.medium.release import (
        Release, ReleaseException, FormalType
        )


CASE1 = '''<?xml version='1.0'?>
<release xmlns='http://vectortron.com/xml/media/media'>
 <type><bluray/></type>
 <publisher>Beta Barn</publisher>
</release>
'''

CASE2 = '''<?xml version='1.0'?>
<release xmlns='http://vectortron.com/xml/media/media'>
 <type></type>
</release>
'''


class TestRelease(unittest.TestCase):
    '''
    Unit tests covering the product release.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.release = Release(xmlroot)

    def test_object_instance(self):
        '''
        Assert Release object is properly created.
        '''
        self.assertIsInstance(self.release, Release)


class TestReleaseException(unittest.TestCase):
    '''
    Unit tests for the release exception conditions.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''

    def test_release_exception(self):
        '''
        Assert that an error will occur if the release
        type is empty.
        '''
        xmlroot = ET.fromstring(CASE2)
        with self.assertRaises(ReleaseException):
            release1 = Release(xmlroot)
            del release1


class TestReleaseType(unittest.TestCase):
    '''
    Unit tests for the release type value.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.release = Release(xmlroot)

    def test_type_value(self):
        '''
        Assert the the product type is set.
        '''
        self.assertEqual(self.release.type, 'bluray')


class TestReleasePublisher(unittest.TestCase):
    '''
    Unit tests for the release publisher value.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        xmlroot = ET.fromstring(CASE1)
        self.release = Release(xmlroot)

    def test_publisher_value(self):
        '''
        Verify the publisher value is set properly.
        '''
        self.assertEqual(self.release.publisher, 'Beta Barn')


class TestFormalType(unittest.TestCase):
    '''
    Unit tests for the FormalType.formal_convert function.
    '''
    def test_correct_type_mapping(self):
        '''
        Assert that a blu-ray type is properly represented.
        '''
        self.assertEqual(FormalType.formal_convert('bluray'), 'Blu-Ray')

    def test_unknown_type_mapping(self):
        '''
        Assert that an unknown type gets the UNKNOWN string value.
        '''
        self.assertEqual(FormalType.formal_convert('squeezebox'), 'UNKNOWN')

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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
import xml.etree.ElementTree as ET
from media.data.media.contents.movie import Movie
from media.data.media.contents.genericv.crew.cast import (
        Cast, Role, Actor, PortraysNamedCharacter, PortraysBackground,
        PortraysAdditionalVoices, PortraysNarrator, PortraysSelf,
        PortraysSelfCharacter, PortraysUnnamedCharacter
        )

CASE1 = '''<?xml version='1.0'?>
<movie xmlns='http://vectortron.com/xml/media/movie'>
 <title>A River Turns Inward</title>
 <crew>
  <cast>
   <role>
    <actor><gn>Marty</gn><fn>Goofus</fn></actor>
    <character>
    <name>
     <prefix>Judge</prefix>
     <gn>Bettle</gn><fn>Gallant</fn>
     <suffix tpe='generational'>Sr.</suffix>
    </name>
    <aspect>voice</aspect>
    </character>
   </role>
   <role>
    <actor><gn>Josh</gn><fn>Gallant</fn></actor>
    <character>
     <name><nick>Travesty</nick></name>
    <variant>old</variant>
    </character>
    <additionalVoices/>
   </role>
   <role>
    <actor><gn>Al</gn><fn>Abama</fn><suffix>Jr.</suffix></actor>
    <background/>
   </role>
   <role>
    <actor><gn>Sally</gn><fn>Meadow</fn></actor>
    <narrator/>
   </role>
   <role>
    <actor archivalFootage='true'>
     <gn>Jerry Lee</gn><mn>Franklin</mn><fn>Thomas</fn>
    </actor>
    <self/>
   </role>
   <role>
     <actor><gn>Paul</gn><fn>Garreth</fn></actor>
     <character>
      <self/>
     </character>
   </role>
   <role>
    <actor><gn>Dewey</gn><fn>Floyd</fn></actor>
    <character>
     <unnamed>Second Cop On The Left</unnamed>
    </character>
   </role>
  </cast>
 </crew>
</movie>
'''


class TestCastObjects(unittest.TestCase):
    '''
    Test for crew level classes.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast

    def test_cast_class_instance(self):
        '''
        Verify crew object is created.
        '''
        self.assertIsInstance(self.cast, Cast)


class TestRoleObject(unittest.TestCase):
    '''
    Role class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_role_class_instance(self):
        '''
        Verify a role object is created.
        '''
        self.assertIsInstance(self.cast[0], Role)

    def test_role_class_portrays_length(self):
        '''
        Verify Role portrays attribute is properly set.
        '''
        self.assertEqual(len(self.cast[0].portrays), 1)

    def test_role_class_order_attribute(self):
        '''
        Verify the Role order attribute is properly set.
        '''
        self.assertEqual(self.cast[1].order, 2)


class TestActorObject(unittest.TestCase):
    '''
    Actor class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_actor_class_instance(self):
        '''
        Verify actor object is present.
        '''
        self.assertIsInstance(self.cast[0].actor, Actor)

    def test_actor_archival_footage_attribute(self):
        '''
        Verify archival_footage attribute gets set.
        '''
        self.assertTrue(self.cast[4].actor.archival_footage)


class TestPortraysNarrator(unittest.TestCase):
    '''
    PortraysNarrator class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_narrator_instrance(self):
        '''
        Verify PortraysNarrator class works.
        '''
        self.assertIsInstance(self.cast[3].portrays[0], PortraysNarrator)


class TestPortraysBackground(unittest.TestCase):
    '''
    PortraysBackground class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_background_instance(self):
        '''
        Verifies PortraysBackground class works.
        '''
        self.assertIsInstance(self.cast[2].portrays[0], PortraysBackground)

    def test_portrays_background_formal_value(self):
        '''
        Verifies PortraysBackground output value.
        '''
        self.assertEqual(str(self.cast[2].portrays[0].formal), 'Background')


class TestPortraysAdditionalVoices(unittest.TestCase):
    '''
    PortraysAdditionalVoices class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_additional_voices_instance(self):
        '''
        Verifies PortraysAdditionalVoices class works.
        '''
        self.assertIsInstance(self.cast[1].portrays[1],
                              PortraysAdditionalVoices)


class TestPortraysSelf(unittest.TestCase):
    '''
    PortraysSelf class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_self_instance(self):
        '''
        Verifies PortraysSelf class works.
        '''
        self.assertIsInstance(self.cast[4].portrays[0], PortraysSelf)


class TestPortraysCharacterSelf(unittest.TestCase):
    '''
    PortraysSelfCharacter class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_character_self_instance(self):
        '''
        Verifies PortraysSelfCharacter class works.
        '''
        self.assertIsInstance(self.cast[5].portrays[0], PortraysSelfCharacter)


class TestPortraysUnnamedCharacter(unittest.TestCase):
    '''
    PortraysUnnamedCharacter class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_unnamed_character_instance(self):
        '''
        Verifies PortraysUnnamedCharacter class works.
        '''
        self.assertIsInstance(self.cast[6].portrays[0],
                              PortraysUnnamedCharacter)

    def test_portrays_unnaned_character_formal_value(self):
        '''
        Verifies formal value is set.
        '''
        self.assertEqual(self.cast[6].portrays[0].formal,
                         'Second Cop On The Left')


class TestPortraysNamedCharacter(unittest.TestCase):
    '''
    CharacterName class tests.
    '''
    def setUp(self):
        xmlroot = ET.fromstring(CASE1)
        self.cast = Movie(xmlroot).crew.cast.cast

    def test_portrays_named_character_instance(self):
        '''
        Verifies PortraysNamedCharacter class works.
        '''
        self.assertIsInstance(self.cast[0].portrays[0], PortraysNamedCharacter)

    def test_named_character_given_name(self):
        '''
        Test creation of CharacterName object.
        '''
        self.assertEqual(self.cast[0].portrays[0].name.matrix['gn'], "Bettle")

    def test_named_character_aspect(self):
        '''
        Test aspect value of character name.
        '''
        self.assertEqual(self.cast[0].portrays[0].aspect, 'voice')

    def test_named_character_variant(self):
        '''
        Test variant value of character name.
        '''
        self.assertEqual(self.cast[1].portrays[0].variant, 'old')


if __name__ == '__main__':
    unittest.main()

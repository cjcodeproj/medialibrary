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

'''
Classes related to cast members and the roles they portray.
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801
# pylint: disable=too-many-instance-attributes

import xml.etree.ElementTree as ET
from media.xml.functions import xs_bool
from media.xml.namespaces import Namespaces
from media.data.nouns import PersonalName
from media.data.media.contents.generic.story.characters import CharacterName
from media.generic.stringtools import build_sort_string


class Cast():
    '''
    Container object for all cast members, or a subset of cast members.
    '''
    def __init__(self, in_element):
        self.cast = []
        if in_element is not None:
            role_count = 1
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'role':
                    self.cast.append(Role(child, role_count))
                    role_count += 1


class Role():
    '''
    A role contains the name of a single actor, and one or
    more portrayal objects.
    '''
    def __init__(self, in_element, in_count):
        self.actor = None
        self.portrays = []
        self.order = in_count
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'actor':
                    self.actor = Actor(child)
                elif tagname == 'self':
                    self.portrays.append(PortraysSelf())
                elif tagname == 'narrator':
                    self.portrays.append(PortraysNarrator())
                elif tagname == 'background':
                    self.portrays.append(PortraysBackground())
                elif tagname == 'additionalVoices':
                    self.portrays.append(PortraysAdditionalVoices())
                elif tagname == 'character':
                    chr_obj = Role.character_dispatcher(child, self.actor)
                    self.portrays.append(chr_obj)

    @classmethod
    def character_dispatcher(cls, in_element, in_actor):
        '''
        Returns a Portrays element based on the inner
        XML structure.
        '''
        tagname = Namespaces.ns_strip(in_element[0].tag)
        if tagname == 'name':
            return PortraysNamedCharacter(in_element)
        if tagname == 'unnamed':
            return PortraysUnnamedCharacter(in_element)
        if tagname == 'self':
            return PortraysSelfCharacter(in_actor)
        return None

    def __str__(self):
        return f"Role object for actor: {str(self.actor)}"


class AbstractActor(PersonalName):
    '''
    Abstract root class for an actor.
    '''


class Actor(AbstractActor):
    '''
    Actor class.
    '''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.archival_footage = False
        if 'archivalFootage' in in_element.attrib:
            if xs_bool(in_element.attrib['archivalFootage']):
                self.archival_footage = True


class AbstractPortrays():
    '''
    Abstract root class for all portrays objects.

    '''
    def __init__(self):
        self.value = ''
        self.formal = ''
        self.sort_value = ''

    def __str__(self):
        return self.value

    def __hash__(self):
        '''
        Hash values are only guaraunteed to be unique
        against other values against the same actor within
        the same role structure.
        '''
        return hash(self.formal)

    def __lt__(self, other):
        return self.sort_value < other.sort_value

    def __rt__(self, other):
        return self.sort_value > other.sort_value

    def __eq__(self, other):
        return self.sort_value == other.sort_value


class PortraysNarrator(AbstractPortrays):
    '''
    Class designating the special role Narrator
    '''
    def __init__(self):
        super().__init__()
        self.value = 'Narrator'
        self.formal = 'Narrator'
        self.sort_value = 'narrator'

    def to_element(self):
        '''
        Generate an empty additionalVoices element.
        '''
        return ET.Element('narrator')


class PortraysSelf(AbstractPortrays):
    '''
    Class for an actor as themselves.
    '''
    def __init__(self):
        super().__init__()
        self.value = 'Self'
        self.formal = 'Self'
        self.sort_value = 'self'


class PortraysBackground(AbstractPortrays):
    '''
    Class for special background character role.
    '''
    def __init__(self):
        super().__init__()
        self.value = 'Background'
        self.formal = 'Background'
        self.sort_value = 'background'

    def to_element(self):
        '''
        Generate an empty background element.
        '''
        return ET.Element('background')


class PortraysAdditionalVoices(AbstractPortrays):
    '''
    Class for special additionalVoices character role.
    '''
    def __init__(self):
        super().__init__()
        self.value = 'Additional Voices'
        self.formal = 'Additional Voices'
        self.sort_value = 'additional voices'


class AbstractPortraysCharacter(AbstractPortrays):
    '''
    Abtract root class of all Portrays objects.
    '''


class PortraysNamedCharacter(AbstractPortraysCharacter):
    '''
    A character with a partial or complete name.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.name = None
        self.aliases = []
        self.variant = None
        self.aspect = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'name':
                self.name = CharacterName(child)
            elif tagname == 'alias':
                self.aliases.append(CharacterName(child))
            elif tagname == 'variant':
                self.variant = child.text
            elif tagname == 'aspect':
                self.aspect = child.text
        self.sort_value = self.name.sort_value
        self._build_formal_name()

    def _build_formal_name(self):
        self.formal = self.name.formal
        if self.variant:
            self.formal += f" ({self.variant})"
        if self.aspect:
            self.formal += f" ({self.aspect})"
        if len(self.aliases) > 0:
            for alias_name in self.aliases:
                self.formal += ' / ' + alias_name.formal


class PortraysSelfCharacter(AbstractPortraysCharacter):
    '''
    Portrayal of a character version of themselves.
    '''
    def __init__(self, in_actor):
        super().__init__()
        self.name = in_actor
        self.sort_value = self.name.sort_value
        self.formal = str(self.name)


class PortraysUnnamedCharacter(AbstractPortraysCharacter):
    '''
    A character that exists, but doesn't have a
    complete or partial name.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.unnamed = ''
        self.variant = None
        self.aspect = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'unnamed':
                self.unnamed = child.text
                self.formal = child.text
                self.sort_value = build_sort_string(child.text)
            elif tagname == 'variant':
                self.variant = child.text
            elif tagname == 'aspect':
                self.aspect = child.text

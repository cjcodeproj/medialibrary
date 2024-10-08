#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
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
Objects for representation of proper nouns used in keywords.
'''

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes

from media.generic.stringtools import build_sort_string
from media.generic.stringtools import chg_ws
from media.xml.namespaces import Namespaces


class AbstractNoun():
    '''
    Root class for all nouns
    '''
    def __init__(self):
        self.value = ''
        self.sort_value = ''
        self.tagname = ''

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        return self.sort_value < other.sort_value

    def __rt__(self, other):
        return self.sort_value > other.sort_value

    def __eq__(self, other):
        return self.sort_value == other.sort_value


def noun_dispatcher(in_element):
    '''
    Deliver an appropriate noun object based on
    the child element sequence discovered in the
    passed element.

    This code only works for crew elements
    where the value is either a personal name
    or a group/entity, or unknown.
    '''
    tagname = Namespaces.ns_strip(in_element[0].tag)
    if tagname == 'grp':
        return Group(in_element[0])
    if tagname == 'ent':
        return Entity(in_element[0])
    if tagname == 'unkn':
        return Noun(in_element[0])
    if tagname in ['prefix', 'pcn', 'pgn', 'gn']:
        return PersonalName(in_element)
    return None


class Noun(AbstractNoun):
    '''
    Simplest class to represent proper nouns
    for Thing, or Event

    value represents the value that is displayed
    sort_value represents the value for sorting
    '''
    def __init__(self, in_element):
        super().__init__()
        if in_element.text:
            self.value = in_element.text
            self.sort_value = self.value.casefold()
        self.tagname = Namespaces.ns_strip(in_element.tag)


class Group(AbstractNoun):
    '''
    A proper noun representing a group of invdividuals.
    '''
    def __init__(self, in_group):
        super().__init__()
        self.value = in_group.text
        self.sort_value = build_sort_string(in_group.text)
        self.tagname = Namespaces.ns_strip(in_group.tag)


class Entity(AbstractNoun):
    '''
    A proper noun representing a collective group.
    '''
    def __init__(self, in_entity):
        super().__init__()
        self.value = in_entity.text
        if 'acronym' in in_entity.attrib:
            self.acronym = in_entity.attrib['acronym']
        self.sort_value = build_sort_string(in_entity.text)
        self.tagname = Namespaces.ns_strip(in_entity.tag)


class Place(AbstractNoun):
    '''
    ProperNoun class for a location

    Has attributes for every possible aspect
    of a location, which is probably going to be
    a problem.
    '''
    def __init__(self, in_place):
        super().__init__()
        self.generic = ''
        self.name = ''
        self.city = ''
        self.county = ''
        self.state = ''
        self.country = ''
        self.planet = ''
        if in_place is not None:
            self.tagname = Namespaces.ns_strip(in_place.tag)
            self._process(in_place)

    def _process(self, in_element):
        first_tag = True
        major = ''
        minor = ''
        for child in in_element:
            if first_tag:
                major = self._build_major_value(child)
                first_tag = False
            else:
                minor = self._build_minor_value(child, minor)
        if minor:
            minor = '(' + minor + ')'
            self.value = major + ' ' + minor
        else:
            self.value = major
        self.sort_value = self.value.casefold()

    def _build_major_value(self, in_element):
        tagname = Namespaces.ns_strip(in_element.tag)
        if tagname == 'generic':
            self.generic = in_element.text
        if tagname == 'name':
            self.name = in_element.text
        elif tagname == 'ci':
            self.city = in_element.text
        elif tagname == 'co':
            self.county = in_element.text
        elif tagname in ['st', 'pr']:
            self.state = in_element.text
        elif tagname == 'cn':
            self.country = in_element.text
        elif tagname == 'planet':
            self.planet = in_element.text
        major = in_element.text
        return major

    def _build_minor_value(self, in_element, minor):
        tagname = Namespaces.ns_strip(in_element.tag)
        if tagname == 'ci':
            self.city = in_element.text
        elif tagname == 'co':
            self.county = in_element.text
        elif tagname in ['st', 'pr']:
            self.state = in_element.text
        elif tagname == 'cn':
            self.country = in_element.text
        elif tagname == 'planet':
            self.planet = in_element.text
        if minor:
            minor += ', ' + in_element.text
        else:
            minor = in_element.text
        return minor


class PersonalName(AbstractNoun):
    '''
    Proper noun for the name of a real person.

    A real person's name will include
    the common components like a given name,
    a family name, and maybe a middle name.

    This class is more heavily used since it
    is the standard name class for crew members
    or any other data types that use a name.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.sort_value = ''
        self.value = ''
        self.given = ''
        self.family = ''
        self.middle = ''
        self.suffix = ''
        self.prefix = ''
        self.pref_complete = ''
        self.pref_given = ''
        if in_element is not None:
            self.tagname = Namespaces.ns_strip(in_element.tag)
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'gn':
                self.given = child.text
            elif tagname == 'fn':
                self.family = child.text
            elif tagname == 'mn':
                self.middle = child.text
            elif tagname == 'suffix':
                self.suffix = child.text
            elif tagname == 'prefix':
                self.prefix = child.text
            elif tagname == 'pgn':
                self.pref_given = child.text
            elif tagname == 'pcn':
                self.pref_complete = child.text
        self._build_value()
        self._build_sort_value()

    def _build_value(self):
        """Construct a printable name."""
        raw = ''
        if self.pref_complete:
            raw = self.pref_complete
        else:
            if self.prefix:
                raw += self.prefix + ' '
            if self.pref_given:
                raw += self.pref_given + ' '
            else:
                if self.given:
                    raw += self.given + ' '
                if self.middle:
                    raw += self.middle + ' '
            if self.family:
                raw += self.family
            if self.suffix:
                raw += ' ' + self.suffix
        self.value = raw

    def _build_sort_value(self):
        """Construct a string for sorting names."""
        raw = ''
        if self.pref_complete:
            raw = chg_ws(self.pref_complete.casefold())
        else:
            if self.family:
                raw = chg_ws(self.family.casefold()) + '_'
                if self.pref_given:
                    raw += chg_ws(self.pref_given.casefold())
                else:
                    raw += chg_ws(self.given.casefold())
                    if self.middle:
                        raw += '_' + chg_ws(self.middle.casefold())
            else:
                raw = chg_ws(self.given.casefold())
                if self.middle:
                    raw += '_' + chg_ws(self.middle)
        self.sort_value = raw

    def __str__(self):
        """The formal string value should be returned."""
        return self.value


class Art(AbstractNoun):
    """
    Proper noun describing a work of art.

    Element contains no child elements, only
    text, plus two optional attributes.
    """
    def __init__(self, in_art_element):
        super().__init__()
        self.art_type = ''
        self.art_year = 0
        if in_art_element is not None:
            self._process(in_art_element)

    def _process(self, in_element):
        art_name = in_element.text.strip()
        self.tagname = Namespaces.ns_strip(in_element.tag)
        if 'type' in in_element.attrib:
            self.art_type = in_element.attrib['type']
        if 'year' in in_element.attrib:
            self.art_year = int(in_element.attrib['year'])
        if self.art_type:
            self.value = art_name + ' (' + self.art_type + ')'
        else:
            self.value = art_name
        self.sort_value = self.value.casefold()

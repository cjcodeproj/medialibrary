#!/usr/bin/env python
'''
Objects for representation of proper nouns used in keywords.
'''

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-branches

from media.xml.namespaces import Namespaces


class Noun():
    '''
    Abstract class for all proper nouns

    '''
    def __init__(self, in_element):
        self.nvalue = in_element.text

    def __str__(self):
        return self.nvalue


class Place():
    '''
    ProperNoun class  for a location
    '''
    def __init__(self, in_place):
        self.name = ''
        self.city = ''
        self.county = ''
        self.state = ''
        self.country = ''
        self.planet = ''
        self.raw = ''
        if in_place is not None:
            self._process(in_place)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'name':
                self.name = child.text
            elif tagname == 'ci':
                self.city = child.text
            elif tagname == 'co':
                self.county = child.text
            elif tagname in ['st', 'pr']:
                self.state = child.text
            elif tagname == 'cn':
                self.country = child.text
            elif tagname == 'planet':
                self.planet = child.text
        self._build_string()

    def _build_string(self):
        ''' This needs to be more flexible'''
        major = ''
        minor = ''
        if self.name:
            major = self.name
        if self.city:
            if major:
                minor += self.city + ', '
            else:
                major = self.city
        if self.county:
            if major:
                minor += self.county + ', '
            else:
                major = self.county
        if self.state:
            if major:
                minor += self.state + ', '
            else:
                major = self.state
        if self.country:
            if major:
                minor += self.country + ', '
            else:
                major = self.country
        if self.planet:
            if major:
                minor += self.planet
            else:
                major = self.planet
        if minor:
            minor = '(' + minor[:-2] + ')'
            self.raw = major + ' ' + minor
        else:
            self.raw = major

    def __str__(self):
        return self.raw


class Name():
    '''
    Proper noun for the name of a real person.

    A real person's name will include
    the common components like a given name,
    a family name, and maybe a middle name.
    '''
    def __init__(self, in_element):
        self.given = ''
        self.family = ''
        self.middle = ''
        self.sort = ''
        self.raw = ''
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'gn':
                self.given = child.text
            if tagname == 'fn':
                self.family = child.text
            if tagname == 'mn':
                self.middle = child.text
        self._build_string()
        self._build_sort()

    def _build_string(self):
        raw = ''
        if self.family:
            raw += self.family + ', '
        if self.given:
            raw += self.given + ' '
        if self.middle:
            raw += self.middle
        self.raw = raw

    def rev_name(self):
        '''Return the name in family, given order'''
        return f"{self.family} {self.given}"

    def _build_sort(self):
        self.sort = self.family.casefold() + '_' \
                    + self.given.casefold() + '_' + self.middle

    def __str__(self):
        return f"{self.given} {self.family}"

    def __repr__(self):
        return f"{self.given} {self.family}"

    def __hash__(self):
        return hash(self.sort)

    def __lt__(self, other):
        return self.sort < other.sort

    def __gt__(self, other):
        return self.sort > other.sort

    def __eq__(self, other):
        return self.sort == other.sort


class CharacterName():
    '''
    Name class for a character name in a movie

    This class is loosely similar to a Name class, but
    there are variations where the character in a
    movie may have names that don't conform to
    the naming conventions of a real person.
    '''
    def __init__(self, in_element):
        self.given = ''
        self.family = ''
        self.middle = ''
        self.narrator = False
        self.chself = False
        if in_element is not None:
            self._process(in_element)

    def is_narrator(self):
        '''Is the role of the narrator'''
        return self.narrator or False

    def plays_self(self):
        '''Is the role playing themselves'''
        return self.chself or False

    def _process(self, in_element):
        '''Build the object based on the data'''
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'gn':
                self.given = child.text
            if tagname == 'fn':
                self.given = child.text
            if tagname == 'mn':
                self.middle = child.text

    def __str__(self):
        return f"{self.given} {self.family}"

    def __repr__(self):
        return f"{self.given} {self.family}"

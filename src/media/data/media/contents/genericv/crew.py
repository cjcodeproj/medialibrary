#!/usr/bin/env python
'''
Classes related to crewmembers of a piece
of visual art, like a movie or television show.
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801

from media.xml.namespaces import Namespaces
from media.data.nouns import Name


class Crew():
    '''
    Main container element for all crew objects.
    '''
    def __init__(self, in_element):
        self.directors = []
        self.editors = []
        self.writers = []
        self.cinemap = []
        self.cast = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'directors':
                self.directors = Directors.load(child)
            if tagname == 'editors':
                self.editors = SimpleCrew.load(child, 'editor')
            if tagname == 'cinemaphotographers':
                self.cinemap = SimpleCrew.load(child, 'cinemaphotographer')
            if tagname == 'writers':
                self.writers = SimpleCrew.load(child, 'writer')
            if tagname == 'cast':
                self.cast = Cast(child)


class Directors():
    '''
    Simple class method to parse director elements.
    '''
    @classmethod
    def load(cls, in_element):
        ''' Load an array of names for a given element in the XML'''
        out = []
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'director':
                    out.append(Name(child))
        return out


class Writers():
    '''
    Class method to parser writer elements, which
    are a little more complex compared to other
    crew elements.
    '''
    @classmethod
    def load(cls, in_element):
        ''' Load an array of writers based on the XML'''
        out = []
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'writer':
                    out.append(Name(child))


class SimpleCrew():
    '''
    Generic crew loader object, which returns
    a list of Name elements.
    '''
    @classmethod
    def load(cls, in_element, desired_tag):
        '''Load an array of names for a given element in the XML'''
        out = []
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == desired_tag:
                    out.append(Name(child))
        return out

    @classmethod
    def output(cls, title, in_list):
        '''Special output formatter to string multiple names together'''
        out_string = ""
        if len(in_list) == 1:
            out_string = f"{title}: {in_list[0]}"
        else:
            out_string = f"{title}"
            for name in in_list:
                out_string += f"{name}. "
            out_string = out_string[:-2]
        return out_string


class Cast():
    '''
    Container object for all cast members, or a subset of cast members.
    '''
    def __init__(self, in_element):
        self.cast = []
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'role':
                    self.cast.append(Role(child))


class Role():
    '''
    A role contains a single actor person, and one or more
    characters portrated by the role.
    '''
    def __init__(self, in_element):
        self.actor = None
        self.portrays = []
        self.billing = 1
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'actor':
                    self.actor = Name(child)
                if tagname == 'as':
                    self.portrays.append(CharacterName(child))
            if 'billing' in in_element.attrib:
                self.billing = int(in_element.attrib['billing'])


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

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
        self.cast = []
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

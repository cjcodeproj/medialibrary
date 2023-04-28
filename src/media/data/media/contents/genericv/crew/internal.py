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
Classes related to crewmembers of a piece
of visual art, like a movie or television show.
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801
# pylint: disable=too-many-instance-attributes

from media.xml.namespaces import Namespaces
from media.data.nouns import PersonalName, noun_dispatcher
from media.data.media.contents.genericv.crew.cast import Cast


class Crew():
    '''
    Main container element for all crew objects.
    '''
    def __init__(self, in_element):
        self.directors = []
        self.editors = []
        self.writers = []
        self.cinemap = []
        self.music = None
        self.cast = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'directors':
                self.directors = Directors.load(child)
            elif tagname == 'editors':
                self.editors = SimpleCrew.load(child, 'editor')
            elif tagname == 'cinemaphotographers':
                self.cinemap = SimpleCrew.load(child, 'cinemaphotographer')
            elif tagname == 'writers':
                self.writers = SimpleCrew.load(child, 'writer')
            elif tagname == 'music':
                self.music = Music(child)
            elif tagname == 'cast':
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
                    out.append(PersonalName(child))
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
                    out.append(PersonalName(child))


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
                    out.append(PersonalName(child))
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


class CrewAssignment():
    '''
    An assignment to a crew position.
    '''
    def __init__(self, tagname, in_element):
        self.title = tagname
        self.uncredited = False
        self.object = noun_dispatcher(in_element)
        if 'uncredited' in in_element.attrib:
            self.uncredited = True

    def __str__(self):
        return str(self.object)


class Music():
    '''
    Container object for all music related staff.
    '''
    def __init__(self, in_element):
        self.allowed = ['composer', 'conductor', 'music']
        self.breakdown = {}
        self.composers = []
        self.conductors = []
        self.music = []
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname in self.allowed:
                # nx_element = child[0]
                crew_obj = CrewAssignment(tagname, child)
                if tagname == 'composer':
                    self.composers.append(crew_obj)
                elif tagname == 'music':
                    self.music.append(crew_obj)
                elif tagname == 'conductor':
                    self.conductors.append(crew_obj)

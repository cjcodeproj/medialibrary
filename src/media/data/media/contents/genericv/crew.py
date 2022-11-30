#!/usr/bin/env python

#
# Copyright 2022 Chris Josephes
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

from media.xml.functions import xs_bool
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
                    child_tag = Namespaces.ns_strip(child[0].tag)
                    if child_tag == 'narrator':
                        self.portrays.append(PortraysNarrator())
                    elif child_tag == 'self':
                        self.portrays.append(PortraysSelf(child))
                    elif child_tag == 'title':
                        self.portrays.append(CharacterTitle(child))
                    else:
                        self.portrays.append(CharacterName(child))
            if 'billing' in in_element.attrib:
                self.billing = int(in_element.attrib['billing'])

    def __str__(self):
        return "Role monster"


class Portrays():
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


class PortraysNarrator(Portrays):
    '''
    Class designating the special role Narrator
    '''
    def __init__(self):
        super().__init__()
        self.value = 'Narrator'
        self.formal = 'Narrator'
        self.sort_value = 'narrator'


class PortraysSelf(Portrays):
    '''
    Class designed for the special role Self
    '''
    def __init__(self, in_element):
        super().__init__()
        self.value = 'Self'
        self.formal = 'Self'
        self.sort_value = 'self'
        ref_tag = in_element[0]
        if 'fictionalVariant' in ref_tag.attrib:
            if xs_bool(ref_tag.attrib['fictionalVariant']):
                self.formal += ' (fictional variant)'
        if 'archivalFootage' in ref_tag.attrib:
            if xs_bool(ref_tag.attrib['archivalFootage']):
                self.formal += ' (archival footage)'


class CharacterTitle(Portrays):
    '''
    Class designed for the special role Title
    '''
    def __init__(self, in_element):
        super().__init__()
        self.value = in_element[0].text
        self.formal = in_element[0].text
        self.sort_value = in_element[0].text.casefold()


class CharacterName(Portrays):
    '''
    Name class for a character name in a movie

    This class is loosely similar to a Name class, but
    there are variations where the character in a
    movie may have names that don't conform to
    the naming conventions of a real person.
    '''
    name_matrix = {
            'gn': 'given',
            'nick': 'nick',
            'mn': 'middle',
            'fn': 'family'
    }

    def __init__(self, in_element):
        super().__init__()
        self.value = ''
        self.chunk = {}
        self.pre_title = ''
        self.post_title = ''
        self.variant = ''
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        '''Build the object based on the data'''
        order = []
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            tagcount = 1
            if tagname in CharacterName.name_matrix:
                if tagname == 'nick':
                    self.chunk[CharacterName.name_matrix[tagname]] = "'" + \
                            child.text + "'"
                else:
                    self.chunk[CharacterName.name_matrix[tagname]] = child.text
                order.append(CharacterName.name_matrix[tagname])
                tagcount += 1
            elif tagname == 'preTitle':
                self.pre_title = child.text
            elif tagname == 'postTitle':
                self.post_title = child.text
            elif tagname == 'variant':
                self.variant = child.text
        self._build_value(order)
        self._build_formal()
        self._build_sort(order)

#    def _process2(self, in_element):
#        '''Build the object based on the data'''
#        for child in in_element:
#            tagname = Namespaces.ns_strip(child.tag)
#            tagcount = 1
#            order = []
#            if tagname == 'self':
#                self.chunk['self'] = "(self)"
#                order = ['self']
#                self._build_value(order)
#                return
#            if tagname == 'narrator':
#                self.chunk['narrator'] = "(narrator)"
#                order = ['narrator']
#                self._build_value(order)
#                return
#            if tagname == 'title':
#                self.chunk['title'] = child.text
#                order = ['title']
#                self._build_value(order)
#                return
#            if tagname == 'nick':
#                self.chunk['nick'] = child.text
#                order.append('nick')
#            if tagname == 'gn':
#                self.chunk['given'] = child.text
#                order.append('given')
#            if tagname == 'mn':
#                self.chunk['middle'] = child.text
#                order.append('middle')
#            if tagname == 'fn':
#                self.chunk['family'] = child.text
#                order.append('family')
#            tagcount += 1
#        self._build_value(order)
#        return

    def _build_value(self, order):
        raw = ''
        for chunk_i in order:
            raw += self.chunk[chunk_i] + ' '
        raw = raw[:-1]
        self.value = raw

    def _build_formal(self):
        raw = ''
        if self.pre_title:
            raw = self.pre_title + ' ' + self.value
        else:
            raw = self.value
        if self.post_title:
            raw += ' ' + self.post_title
        if self.variant:
            raw += ' (' + self.variant + ')'
        self.formal = raw

    def _build_sort(self, order):
        order = ['family', 'given', 'middle']
        raw = ''
        for o_i in order:
            if o_i in self.chunk:
                raw += self.chunk[o_i].casefold() + '_'
        raw = raw[:-1]
        self.sort_value = raw

#    def complete(self):
#        out = ''
#        if self.pre_title:
#            out = self.pre_title + ' ' + self.value
#        else:
#            out = self.value
#        if self.post_title:
#            out += ' ' + self.post_title
#        if self.variant:
#            out += ' (' + self.variant + ')'
#        return out

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.chunk['given']} {self.chunk['family']}"

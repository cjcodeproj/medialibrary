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
Object classes for characters in a story.
'''

# pylint: disable=too-few-public-methods


from media.xml.namespaces import Namespaces
from media.generic.stringtools import build_sort_string


class AbstractCharacter():
    '''
    Abstract root class of all characters.
    '''
    def __init__(self):
        self.sort_value = ''


class CharacterSelf(AbstractCharacter):
    '''
    A character based on... someone??
    '''
    def __init__(self):
        super().__init__()
        self.name = ''
        # How do we get the actor name here?


class NamedCharacter(AbstractCharacter):
    '''
    A character with a name.
    '''
    def __init__(self):
        super().__init__()
        self.name = ''


class UnnamedCharacter(AbstractCharacter):
    '''
    A character without a name.
    '''
    def __init__(self):
        super().__init__()
        self.name = ''


class CharacterName():
    '''
    Class for the structure of a character name.

    Character names are more loose/chaotic versus
    PersonalNames because details can be intentionally
    missing.

    '''
    name_tags = ['pgn', 'pcn', 'gn', 'nick', 'mn', 'fn']
    sort_order = ['fn', 'pgn', 'gn', 'mn']

    def __init__(self, in_element):
        self.value = ''
        self.formal = ''
        self.sort_value = ''
        self.matrix = {}
        self.prefix = ''
        self.suffix = ''
        self.addendum = ''
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        order = []
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname in CharacterName.name_tags:
                if tagname == 'nick':
                    self.matrix[tagname] = "'" + child.text + "'"
                else:
                    self.matrix[tagname] = child.text
                order.append(tagname)
            elif tagname == 'prefix':
                self.prefix = child.text
            elif tagname == 'suffix':
                self.suffix = child.text
            elif tagname == 'addendum':
                self.addendum = child.text
        self._build_value(order)
        self._build_formal()
        self._build_sort()

    def _build_value(self, in_order):
        raw = ''
        for tag_name in in_order:
            raw += self.matrix[tag_name] + ' '
        raw = raw[:-1]
        self.value = raw

    def _build_formal(self):
        raw = ''
        if self.prefix:
            raw = self.prefix + ' ' + self.value
        else:
            raw = self.value
        if self.suffix:
            raw += ' ' + self.suffix
        if self.addendum:
            raw += ' (' + self.addendum + ')'
        self.formal = raw

    def _build_sort(self):
        raw = ''
        if 'pcn' in self.matrix:
            raw = build_sort_string(self.matrix['pcn'])
        else:
            for n_sort in CharacterName.sort_order:
                if n_sort in self.matrix:
                    raw += self.matrix[n_sort].casefold() + '_'
            raw = raw[:-1]
        self.sort_value = raw

    def __str__(self):
        return f"{self.value}"

    def __rept__(self):
        return f"{self.matrix}"

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
Keywords module
'''

# pylint: disable=too-few-public-methods
# pylint: disable=consider-using-dict-items

from media.data.nouns import Noun, Name, Place, Art
from media.xml.namespaces import Namespaces


class Keywords():
    '''
    Main container object for a list of keyword objects
    Main container class is a hash table of arrays, which can get tricky.

    Keywords are either GenericKeyword objects, or ProperNoun objects.

    Every keyword has an integer relevance value to signify importance.
    The values range from 1 (most important) to 5 (least important) with
    the default value being 3.

    All keywords are kept in an array of pools (known as collections
    in the XML schema.  If no collections is defined for a keyword,
    it goes in the 'generic' pool.

    Groups are a feature of the XML schema that allow multiple
    keyword objects to share the same relevance value, or the
    same collection value.
    '''
    def __init__(self, in_kw_element):
        '''Initialize keyword bundle'''
        self.pools = {}
        if in_kw_element is not None:
            self._process(in_kw_element)

    def all(self):
        '''Return all keywords in a sorted array'''
        out = []
        for pool_n in self.pools:
            out.extend(self.pools[pool_n])
        return sorted(out)

    def pool_list(self):
        '''Returns a list of keyword pools'''
        return self.pools.keys()

    def all_by_pools(self):
        '''Returns a dictionary of keywords, ordered by the pool name'''
        out_p = {}
        for pool_n in self.pools:
            out_p[pool_n] = sorted(self.pools[pool_n])
        return out_p

    def _process(self, in_kw_element):
        for child in in_kw_element:
            tname = Namespaces.ns_strip(child.tag)
            if tname == 'generic':
                self._add_single_kw(child)
            elif tname == 'properNoun':
                self._add_proper_noun(child)
            elif tname == 'group':
                self._add_group(child)

    def _add_single_kw(self, child):
        if child.text:
            if child.text.strip() != '':
                gen_kw = GenericKeyword(child)
                self._add_to_pool(gen_kw)

    def _add_proper_noun(self, child):
        prn_kw = ProperNounKeyword(child)
        self._add_to_pool(prn_kw)

    def _add_to_pool(self, kw_object):
        pool = kw_object.pool
        if pool in self.pools:
            self.pools[pool].append(kw_object)
        else:
            self.pools[pool] = [kw_object]

    def _add_group(self, group_element):
        pool = None
        relevance = None
        if 'collection' in group_element.attrib:
            pool = group_element.attrib['collection']
        if 'relevance' in group_element.attrib:
            relevance = int(group_element.attrib['relevance'])
        for child in group_element:
            tname = Namespaces.ns_strip(child.tag)
            if tname == 'generic':
                if child.text:
                    if child.text.strip() != '':
                        gen_kw = GenericKeyword(child)
                        if pool:
                            gen_kw.pool = pool
                        if relevance:
                            gen_kw.relevance = relevance
                        self._add_to_pool(gen_kw)
            if tname == 'properNoun':
                prn_kw = ProperNounKeyword(child)
                if pool:
                    prn_kw.pool = pool
                if relevance:
                    prn_kw.relevance = relevance
                self._add_to_pool(prn_kw)


class AbstractKeyword():
    '''
    Parent class that both GenericKeyword and ProperNounKeyword inherit from
    '''
    def __init__(self, in_element):
        self.value = ''
        self.sort_value = ''
        self.type = ''
        self.relevance = 3
        self.synonym = None
        self.pool = 'generic'
        self.clarification = None
        self._process_attributes(in_element)

    def _process_attributes(self, in_element):
        if 'relevance' in in_element.attrib:
            self.relevance = int(in_element.attrib['relevance'])
        if 'collection' in in_element.attrib:
            self.pool = in_element.attrib['collection']
        if 'clarification' in in_element.attrib:
            self.clarification = in_element.attrib['clarification']
        if 'synonym' in in_element.attrib:
            self.synonym = in_element.attrib['synonym']

    def detail(self):
        '''
        Return detailed data on the keyword
        '''
        return self.type + '/' + self.value

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        '''
        Sorting for all keywords is tricier, becase
        the relevance value has to be accounted for. If
        the keyword "banana" has a lower relevance value than
        the keyword "apple", then "banana" comes first in the
        sort evaluation.

        All subclasses of AbstractKeyword should inherit
        this mechanism, and the subclasses should be
        able to compare themselves to one another.
        '''
        if self.relevance == other.relevance:
            return self.sort_value < other.sort_value
        return self.relevance < other.relevance

    def __gt__(self, other):
        if self.relevance == other.relevance:
            return self.sort_value > other.sort_value
        return self.relevance > other.relevance

    def __eq__(self, other):
        if self.relevance == other.relevance:
            return self.sort_value == other.sort_value
        return False


class GenericKeyword(AbstractKeyword):
    '''
    A generic keyword is a simple string that doesn't have any
    unique traits, compared to a ProperNounKeyword.  It's
    value could represent a common noun, or a verb, or
    almost anything.

    It has values for relevance, a synonym string, a
    clarification string, and a pool assignments.

    '''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.value = in_element.text
        self.sort_value = self.value.casefold()
        self.type = 'generic'

    def __str__(self):
        return self.value


class ProperNounKeyword(AbstractKeyword):
    '''
    Proper name keyword, which is tricker, because there is
    an embedded pproper noun inside the element that has to
    be accounted for, alongside the attributes of the
    keyword properNoun element.
    '''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type = 'properNoun'
        self._process(in_element)
        self.sort_value = str(self.value.sort_value).casefold()

    def _process(self, in_element):
        if in_element is not None:
            child = in_element[0]
            tagname = Namespaces.ns_strip(child.tag)
            self.tagtype = tagname
            if tagname in ['thing', 'entity', 'group', 'event']:
                self.value = Noun(child)
            elif tagname == 'person':
                self.value = Name(child)
            elif tagname == 'place':
                self.value = Place(child)
            elif tagname == 'art':
                self.value = Art(child)

    def detail(self):
        return self.type + '/' + self.tagtype + '/' + str(self.value)

    def __str__(self):
        return str(self.value)

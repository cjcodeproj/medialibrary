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

'''The medium release class'''

# pylint: disable=too-few-public-methods
# pylint: disable=consider-using-dict-items

import sys
from media.xml.namespaces import Namespaces


class AbstractPackage():
    '''Abstract class for packaging.'''
    def __init__(self):
        self.media = []
        self.type_s = 'UNDEF'

    def subcontainers_list(self):
        '''
        Return all containers in a
        package.
        '''
        out = []
        for m_item in self.media:
            if issubclass(m_item.__class__, AbstractCase):
                out.append(m_item)
        return out

    def media_string_count_hash(self):
        '''
        Iterates through all objects in
        the inventory.  If the object is a media
        type, it is placed in a hash table to
        record the type, and build an inventory
        count.
        '''
        m_table = {}
        for m_item in self.media:
            if issubclass(m_item.__class__, AbstractMedia):
                media_str = str(m_item)
                if media_str in m_table:
                    m_table[media_str] += 1
                else:
                    m_table[media_str] = 1
        return m_table

    def media_string_count_list(self):
        '''
        Return a formatted list of strings reporitng
        inventory breakdown.  IE, if a container has
        two DVDs and a blu-ray, it returns two strings,
        one for each item type, with a count integer
        if the count is greater than 1.
        '''
        m_list = []
        m_table = self.media_string_count_hash()
        for m_item in m_table:
            if m_table[m_item] > 1:
                m_list.append(f"{m_item} ({m_table[m_item]})")
            else:
                m_list.append(f"{m_item}")
        return m_list

    def __str__(self):
        return self.type_s


class AbstractCase(AbstractPackage):
    '''Abstract 2nd level case.'''


class Box(AbstractPackage):
    '''Product case that can hold other cases.'''
    def __init__(self, in_element):
        super().__init__()
        self.type_s = 'Box'
        self._process(in_element)

    def _process(self, in_element):
        '''
        The _process method for Box is unique
        because it's possible for a box
        to contain other containers.

        This method could conceivably be
        moved to an abstract class if
        there were other weird package
        options that could contain other cases.
        '''
        if len(in_element) > 0:
            for child in in_element:
                child_tag = Namespaces.ns_strip(child.tag)
                if child_tag in Containers:
                    sub_c = Containers[child_tag](child)
                    self.media.append(sub_c)


class Case(AbstractCase):
    '''Generic product case.'''
    def __init__(self, in_element):
        super().__init__()
        self.type_s = 'Case'
        self.slipcover = False
        self._process(in_element)

    def _process(self, in_element):
        '''
        Identify all media or other pieces inside
        the container and put them in the media
        array.
        '''
        if 'slipcover' in in_element.attrib:
            self.slipcover = True
        if len(in_element) > 0:
            for child in in_element:
                child_tag = Namespaces.ns_strip(child.tag)
                if child_tag in Media:
                    sub_m = Media[child_tag](child)
                    self.media.append(sub_m)


class Snapcase(AbstractCase):
    '''old style cardboard and plastic case'''
    def __init__(self, in_element):
        super().__init__()
        self.type_s = 'Snapcase'
        self._process(in_element)

    def _process(self, in_element):
        '''
        Identify all media or other pieces inside
        the container and put them in the media
        array.
        '''
        if len(in_element) > 0:
            for child in in_element:
                c_tag = Namespaces.ns_strip(child.tag)
                if c_tag in Media:
                    sub_m = Media[c_tag](child)
                    self.media.append(sub_m)


class DigiBook(AbstractCase):
    '''media case that typically has 1 disc and 1 book.'''
    def __init__(self, in_element):
        super().__init__()
        self.type_s = 'Digibook'
        self._process(in_element)

    def _process(self, in_element):
        '''
        Identify all media or other pieces inside
        the container and put them in the media
        array.
        '''
        if len(in_element) > 0:
            for child in in_element:
                c_tag = Namespaces.ns_strip(child.tag)
                if c_tag in Media:
                    sub_m = Media[c_tag](child)
                    self.media.append(sub_m)


class Envelope(AbstractCase):
    '''cardboard envelope.'''
    def __init__(self, in_element):
        super().__init__()
        self.type_s = 'Envelope'
        self._process(in_element)

    def _process(self, in_element):
        '''
        Identify all media or other pieces inside
        the container and put them in the media
        array.
        '''
        if len(in_element) > 0:
            for child in in_element:
                c_tag = Namespaces.ns_strip(child.tag)
                if c_tag in Media:
                    sub_m = Media[c_tag](child)
                    self.media.append(sub_m)


class AbstractMedia():
    '''Abstract media object.'''
    def __init__(self, in_element):
        self.media_id = 0
        self.type_s = 'UNDEF'
        if in_element:
            pass

    def __str__(self):
        return self.type_s


class VideoDiscMedia(AbstractMedia):
    '''Video disc class.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.radius = 5


class DVD(VideoDiscMedia):
    '''DVD class.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type_s = 'DVD'


class BluRay(VideoDiscMedia):
    '''Blu-Ray disc class.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type_s = 'Blu-Ray'


class UltraHD(VideoDiscMedia):
    '''UltraHD disc class.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type_s = 'UltraHD'


class Booklet(AbstractMedia):
    '''Booklet  class.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type_s = 'Booklet'


class CodeSheet(AbstractMedia):
    '''Code sheet for downloading media.'''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.type_s = 'Codesheet'


#
# The following dictionaries associate the element names
# with the appropriate classes they represent.
#


Containers = {
        'case': getattr(sys.modules[__name__], 'Case'),
        'snapcase': getattr(sys.modules[__name__], 'Snapcase'),
        'digibook': getattr(sys.modules[__name__], 'DigiBook'),
        'envelope': getattr(sys.modules[__name__], 'Envelope'),
        }

Media = {
        'ultrahd': getattr(sys.modules[__name__], 'UltraHD'),
        'bluray': getattr(sys.modules[__name__], 'BluRay'),
        'dvd': getattr(sys.modules[__name__], 'DVD'),
        'booklet': getattr(sys.modules[__name__], 'Booklet'),
        'codesheet': getattr(sys.modules[__name__], 'CodeSheet'),
        }

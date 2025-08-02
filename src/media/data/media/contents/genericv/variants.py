#!/usr/bin/env python

#
# Copyright 2025 Chris Josephes
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
Code to handle technical aspects of a vidsual format media
(movies, television)
'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces
from media.data.media.contents.genericv.technical import Technical


class VariantPool():
    '''
    A class to handle variant loading.
    '''
    @classmethod
    def read_variants(cls, in_element):
        '''
        Read a variants element structure and create
        the variant child objects.
        '''
        variants = []
        if in_element is not None:
            for child in in_element:
                tagname = Namespaces.ns_strip(child.tag)
                if tagname == 'original':
                    variants.append(OriginalVariant(child))
                elif tagname == 'variant':
                    variants.append(Variant(child))
        return variants


class AbstractVariant():
    '''
    Abstract Variant class.
    '''
    def __init__(self):
        self.id = ''
        self.name = ''
        self.notes = ''

    def _process_xml_stream(self, in_element):
        if 'id' in in_element.attrib:
            self.id = in_element.attrib['id']
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'name':
                self.name = child.text
            elif tagname == 'notes':
                self.notes = child.text


class OriginalVariant(AbstractVariant):
    '''
    Original type Variant class
    '''
    def __init__(self, in_element):
        super().__init__()
        if in_element is not None:
            self._process_xml_stream(in_element)


class Variant(AbstractVariant):
    '''
    Regular type Variant class.
    '''

    def __init__(self, in_element):
        super().__init__()
        self.techincal = None
        if in_element is not None:
            self._process_xml_stream(in_element)

    def _process_xml_stream(self, in_element):
        super()._process_xml_stream(in_element)
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'technical':
                self.technical = Technical(child)

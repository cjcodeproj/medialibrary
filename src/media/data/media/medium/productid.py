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

'''The product identification classes'''

# pylint: disable=too-few-public-methods

from media.xml.functions import xs_bool
from media.xml.namespaces import Namespaces


class ProductId():
    '''Structure for all elements pertaining to product identification.'''
    def __init__(self, in_chunk):
        self.barcodes = []
        self.skus = []
        self.others = []
        self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            if child.tag == Namespaces.nsf('media') + 'barcode':
                self.barcodes.append(Barcode(child))
            elif child.tag == Namespaces.nsf('media') + 'sku':
                self.skus.append(SKU(child))
            elif child.tag == Namespaces.nsf('media') + 'other':
                self.others.append(OtherId(child))


class Barcode():
    '''Representation for a barcode on a piece of physical media.'''
    def __init__(self, in_element):
        self.value = None
        self.type = None
        self.scanlines = True
        if in_element.text:
            chunk = in_element.text.strip()
            if chunk != '':
                self.value = chunk
        if 'type' in in_element.attrib:
            self.type = in_element.attrib['type'].strip()
        if 'scanlines' in in_element.attrib:
            self.scanlines = xs_bool(in_element.attrib['scanlines'])

    def __str__(self):
        return f"{self.value} ({self.type})"


class SKU():
    '''Representation of a Retailer SKU for a physical piece of media.'''
    def __init__(self, in_element):
        self.value = None
        self.retailer = ''
        self.type = None
        if in_element.text:
            chunk = in_element.text.strip()
            if chunk != '':
                self.value = chunk
        if 'retailer' in in_element.attrib:
            self.retailer = in_element.attrib['retailer'].strip()
        if 'type' in in_element.attrib:
            self.type = in_element.attrib['type'].strip()

    def __str__(self):
        return f"{self.value} ({self.retailer})"


class OtherId():
    '''Other ID values, like a "Proof Of Purchase".'''
    def __init__(self, in_element):
        self.name = None
        self.values = []
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'name':
                self.name = child.text.strip()
            if child.tag == Namespaces.nsf('media') + 'value':
                self.values.append(child.text.strip())

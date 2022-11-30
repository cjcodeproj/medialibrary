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

from media.xml.namespaces import Namespaces
import media.data.media.medium.inventory as MI


class ProductSpecs():
    '''Structure for all elements pertaining to product identification.'''
    def __init__(self, in_chunk):
        self.inventory = None
        self.dimensions = None
        self._process(in_chunk)

    def _process(self, in_chunk):
        for child in in_chunk:
            if child.tag == Namespaces.nsf('media') + 'inventory':
                self.inventory = Inventory(child)
            if child.tag == Namespaces.nsf('media') + 'dimensions':
                self.dimensions = Dimensions(child)


class Inventory():
    '''
    Inventory of all items in the package.
    '''
    def __init__(self, in_element):
        self.inventory = []
        self._process(in_element)

    def _process(self, in_element):
        if len(in_element) > 0:
            for child in in_element:
                new_t = Namespaces.ns_strip(child.tag)
                if new_t == 'box':
                    self.inventory.append(MI.Box(child))
                if new_t in MI.Containers:
                    sub_c = MI.Containers[new_t](child)
                    # sub_c.__init__(child)
                    self.inventory.append(sub_c)

    def __str__(self):
        out = ''
        for itm in self.inventory:
            out += f"{itm!s}"
        return out


class Dimensions():
    '''
    Overall dimensions of the physical media.
    '''
    def __init__(self, in_element):
        self.length = 0.0
        self.width = 0.0
        self.height = 0.0
        self.weight = 0.0
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'size':
                self._process_size(child)
            elif child.tag == Namespaces.nsf('media') + 'weight':
                self._process_weight(child)

    def _process_size(self, in_element):
        '''
        Explanation on legth, width, and height:

        length and width represent the measurments of
        the package if it was upright and lying flat on its back, which
        means that height refers to the height of the spine.

        In most measurements, length is used to refer to the
        higher value of measurement between length and width.

        Lying flat on its back, a typical US blu-ray case is 6.75
        inches in length (or 6.75 inches tall), and
        5.4 inches in width.  That leaves the final
        dimension as height, which is usually 0.5 inches.

        The dimensions only get set if both length and
        width are positive values.  The height value
        is an optional value because some storage
        units, like Envelopes have a height value
        so low, it's almost not worth recording.
        '''
        if 'length' in in_element.attrib:
            length = float(in_element.attrib['length'])
        if 'width' in in_element.attrib:
            width = float(in_element.attrib['width'])
        if 'height' in in_element.attrib:
            height = float(in_element.attrib['height'])
        if length > 0 and width > 0:
            self.length = length
            self.width = width
            if height > 0:
                self.height = height

    def _process_weight(self, in_element):
        if in_element.text:
            weight = float(in_element.text)
            if weight > 0:
                self.weight = weight

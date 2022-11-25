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

'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces
from media.data.dates import ExactDate, RangeDate


class Instance():
    '''
    Instance tracks data on a single physical copy of
    media.  It tracks a local filing id value, an
    acquisition, and a value tracking the condition
    of the instance.
    '''
    def __init__(self, in_element):
        self.local_id = None
        self.acquisition = None
        self.condition = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'localId':
                self.local_id = child.text
            elif child.tag == Namespaces.nsf('media') + 'acquisition':
                self.acquisition = Aquisition(child)
            elif child.tag == Namespaces.nsf('media') + 'condition':
                self.condition = Condition(child)


class Aquisition():
    '''
    Acquisition details the process of how an instance was acquired.
    All aquisitions have a date, and further data that is either
    a purchase or a gift.
    '''
    def __init__(self, in_element):
        self.date = None
        self.acq = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'date':
                date_element = child[0]
                if date_element.tag == Namespaces.nsf('media') + 'exact':
                    self.date = ExactDate(date_element)
                elif date_element.tag == Namespaces.nsf('media') + 'from':
                    self.date = RangeDate(date_element, child[1])
            if child.tag == Namespaces.nsf('media') + 'purchase':
                self.acq = Purchase(child)
            elif child.tag == Namespaces.nsf('media') + 'gift':
                self.acq = Gift(child)

    def __str__(self):
        return f"{self.acq!s}"


class Gift():
    '''
    An instance that was acquired as a gift.
    '''
    def __init__(self, in_element):
        self.g_from = ''
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'from':
                self.g_from = child.text

    def __str__(self):
        return f"Gift (from {self.g_from})"


class Purchase():
    '''
    A pysical media instance that was purchased.
    '''
    def __init__(self, in_element):
        self.retailer = ''
        self.location = ''
        self.price = 0.0
        self.quality = ''
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'retailer':
                self.retailer = child.text
            if child.tag == Namespaces.nsf('media') + 'location':
                self.location = child.text
            if child.tag == Namespaces.nsf('media') + 'price':
                self.price = float(child.text)
            if child.tag == Namespaces.nsf('media') + 'quality':
                self.quality = Namespaces.ns_strip(child[0].tag)

    def __str__(self):
        out = 'Purchase'
        if self.price > 0:
            out += f" {self.price:.2f}"
        r_string = self.retailer.strip()
        if r_string:
            out += f" ({r_string})"
        return out


class Condition():
    '''
    Identifies the condition of the physical media.
    '''
    def __init__(self, in_element):
        self.status = ''
        self.notes = ''
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'status':
                self.status = Namespaces.ns_strip(child[0].tag)
            if child.tag == Namespaces.nsf('media') + 'notes':
                self.notes = child.text

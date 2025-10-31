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

'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces

from media.data.media.medium.device import BaseDevice, MediumDeviceMap
from media.data.media.medium.release import (
        FormalType, Release, ReleaseException)
from media.data.media.medium.productid import ProductId
from media.data.media.medium.productspecs import ProductSpecs


class Medium():
    '''Medium object - the physical thing'''
    def __init__(self, in_element):
        self.release = None
        self.device = None
        self.new_device_used = False
        self.product_id = None
        self.product_specs = None
        self._process_xml_stream(in_element)

    def _process_xml_stream(self, in_element):
        for child in in_element:
            e_tag = Namespaces.ns_strip(child.tag)
            if e_tag in MediumDeviceMap.f_map:
                self.new_device_used = True
                self.device = BaseDevice(child)
            elif e_tag == 'release' and self.new_device_used is False:
                try:
                    self.release = Release(child)
                except ReleaseException as rel:
                    raise MediumException(rel.message) from rel
            elif e_tag == 'productId':
                self.product_id = ProductId(child)
            elif e_tag == 'productSpecs':
                self.product_specs = ProductSpecs(child)


class MediumException(Exception):
    '''
    Exceptions related to the medium object.
    '''
    def __init__(self, in_message):
        super().__init__(in_message)
        self.message = in_message

    def __str__(self):
        return self.message


def get_medium_type(in_medium):
    '''
    Simple fumction to get medium type value.
    '''
    f_type = ''
    m_type = ''
    if in_medium.device:
        f_type = in_medium.device.type_name
        m_type = MediumDeviceMap.formal_convert(f_type)
    elif in_medium.release:
        f_type = in_medium.release.type
        m_type = FormalType.formal_convert(f_type)
    else:
        m_type = 'UNKNOWN'
    return m_type

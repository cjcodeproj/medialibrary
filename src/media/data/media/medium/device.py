#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
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
# pylint: disable=R0801

from media.xml.namespaces import Namespaces


class MediumDeviceMap():
    '''Static output representation on media types.'''
    f_map = {
            "audiocd": "Audio CD",
            "casette": "Casette",
            "record": "Record",
            "dvd": "DVD",
            "bluray": "Blu-Ray",
            "bluray3d": "Blu-Ray 3D",
            "hddvd": "HD-DVD",
            "ultrahd": "Ultra HD",
            "vhs": "VHS",
            "betamax": "Betamax"
        }

    @classmethod
    def formal_convert(cls, in_type):
        '''
        Return the type value in a more friendly string.
        '''
        if in_type in cls.f_map:
            return MediumDeviceMap.f_map[in_type]
        return "UNKNOWN"


class AbstractDevice():
    '''
    Abstract device class.  Identifies the type of physical media.
    '''
    def __init__(self):
        self.type_name = None
        self.formal_name = None


class BaseDevice(AbstractDevice):
    '''
    Stump class for device.  More device classes will be added later.
    '''
    def __init__(self, in_element):
        super().__init__()
        if in_element is not None:
            self._process_xml_stream(in_element)

    def _process_xml_stream(self, in_element):
        e_tag = Namespaces.ns_strip(in_element.tag)
        if e_tag in MediumDeviceMap.f_map:
            self.type_name = e_tag
            self.formal_name = MediumDeviceMap.f_map[e_tag]

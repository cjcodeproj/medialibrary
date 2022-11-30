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


class Release():
    '''
    The release is the basic description of a physical release
    of a work of art.

    For a movie that could be a film canister, or a DVD.
    For a story the release could be a book.
    For a piece of music, that release could be an audio CD.

    The release describes the type of release it is, who
    published it, and the date it was released.
    '''
    def __init__(self, in_element):
        self.type = None
        self.publisher = None
        self._process(in_element)

    def _process(self, in_element):
        '''
        The publisher tag is easy to handle.
        The type tag is tricky because it can only
        contain a single XML element.
        '''
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'type':
                if len(child) == 1:
                    self.type = Namespaces.ns_strip(child[0].tag)
            elif child.tag == Namespaces.nsf('media') + 'publisher':
                self.publisher = child.text
        if self.type is None:
            raise ReleaseException('No media release type set.')


class ReleaseException(Exception):
    '''
    The ReleaseException class is thrown when there is
    incomplete data in the Release data structure.
    '''
    def __init__(self, in_message):
        super().__init__(in_message)
        self.message = in_message

    def __str__(self):
        return self.message


class FormalType():
    '''Static output representation on media types.'''
    f_map = {
            "cd": "CD",
            "casette": "Casette",
            "record": "Record",
            "dvd": "DVD",
            "bluray": "Blu-Ray",
            "bluray3d": "Blu-Ray 3D",
            "hddvd": "HD-DVD",
            "ultrahd": "Ultra HD",
            "vhs": "VHS",
            "beta": "Betamax"
        }

    @classmethod
    def formal_convert(cls, in_type):
        '''
        Return the type value in a more friendly string.
        '''
        if in_type in cls.f_map:
            return FormalType.f_map[in_type]
        return "UNKNOWN"

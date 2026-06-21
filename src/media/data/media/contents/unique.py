#!/usr/bin/env python

#
# Copyright 2026 Chris Josephes
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
Abstract object class for the unique key.
'''

# pylint: disable=too-few-public-methods

import zlib


class AbstractUniqueKey():
    '''
    A unique identifier string, that is designed
    to be easily readable and also suitable for
    use as a part of a filename or a URI.
    '''
    def __init__(self):
        self.c_name = None.__class__.__name__.lower()
        self.title = ''
        self.value = ''
        self.extra = ''
        self.year = ''
        self.hash = KeyHash()

    @staticmethod
    def crc32enc(in_list):
        '''
        Generate a 32 bit CRC value from the passed data.
        '''
        in_str = '-'.join(in_list)
        return zlib.crc32(bytes(in_str, 'utf-8'))

    @staticmethod
    def concat(in_title, in_year, in_hash):
        '''
        Build the basic string.
        '''
        out = ''
        if not in_year:
            out = in_title + '-' + str(in_hash)
        else:
            out = in_title + '-' + in_year + '-' + str(in_hash)
        return out

    def full(self):
        '''
        Return a fuller unique string with class information.
        '''
        return self.c_name + '/' + self.value

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.full() == other.full()

    def __hash__(self):
        return hash(self.full())


class KeyHash():
    '''
    A calculated portion of the unique identifier.
    '''
    def __init__(self):
        self._low = 0
        self._high = 0

    @property
    def low(self):
        '''
        Get/set the low value of the hash.
        '''
        return self._low

    @low.setter
    def low(self, in_value):
        self._low = in_value

    @property
    def high(self):
        '''
        Get/set the high value of the hash.
        '''
        return self._high

    @high.setter
    def high(self, in_value):
        self._high = in_value

    def full(self):
        '''
        Return a 64 bit integer merging the high and low values.

        I learned this from using MRTG on high speed routers.
        '''
        return self._high << 32 | self._low

    def __str__(self):
        return f"{self._high:08x}{self._low:08x}"

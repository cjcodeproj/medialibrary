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

'''Unit tests for movie unique key class.'''

# pylint: disable=R0801

import unittest
from media.data.media.contents.unique import KeyHash

LOW = 0x00000001
HGH = 0x00000002
FULL = HGH << 32 | LOW
HEXSTR = '0000000200000001'


class TestKeyHashCase(unittest.TestCase):
    '''
    Unit tests for testing the KeyHash class.
    '''
    def setUp(self):
        '''
        Set up unit tests.
        '''
        self.keyhash = KeyHash()
        self.keyhash.low = LOW
        self.keyhash.high = HGH

    def test_object_instance(self):
        '''
        Assert Classification instance is created.
        '''
        self.assertIsInstance(self.keyhash, KeyHash)

    def test_full_value(self):
        '''
        Assert the hashed value is correct.
        '''
        self.assertEqual(self.keyhash.full(), FULL)

    def test_str_value(self):
        '''
        Assert the hexadecimal value is correct.
        '''
        self.assertEqual(str(self.keyhash), HEXSTR)


if __name__ == '__main__':
    unittest.main()

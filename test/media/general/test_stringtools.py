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

'''Unit tests for code handling titles.'''

# pylint: disable=R0801

import unittest
from media.general.stringtools import (
        transform_string, trans_str_ws)


class TestStringToolsCase(unittest.TestCase):
    '''
    Test string testing methods.
    '''
    def test_transform_string(self):
        '''
        Test the removal of punctuation from a string.
        '''
        str_in = "Barry's Condition"
        str_out = "barrys condition"
        self.assertEqual(transform_string(str_in), str_out)

    def test_trans_str_ws(self):
        '''
        Test the removal of punctuation and change of
        whitespace in a string.
        '''
        str_in = "Jennifer's Body"
        str_out = "jennifers_body"
        self.assertEqual(trans_str_ws(str_in), str_out)


if __name__ == '__main__':
    unittest.main()

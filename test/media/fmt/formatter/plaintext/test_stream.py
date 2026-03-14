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

'''Unit tests for classification classes.'''

# pylint: disable=R0801

import unittest
from media.fmt.formatter.plaintext.stream import PlainTextStream


class TestCSVStream(unittest.TestCase):
    '''
    Test CSVStream object.
    '''
    def setUp(self):
        self.plaintext_stream = PlainTextStream()

    def test_instance_class(self):
        '''
        Test the variable is the proper class.
        '''
        self.assertIsInstance(self.plaintext_stream, PlainTextStream)

    def test_mime_type(self):
        '''
        Test the mime value is correct.
        '''
        self.assertEqual(self.plaintext_stream.mime_type, 'text/plain')

    def test_extension(self):
        '''
        Test the file extension value.
        '''
        self.assertEqual(self.plaintext_stream.extension, 'txt')

    def test_mime_header(self):
        '''
        Test the HTTP Content-Type header.
        '''
        self.assertEqual(self.plaintext_stream.mime_header(),
                         "Content-Type: text/plain\n")


if __name__ == '__main__':
    unittest.main()

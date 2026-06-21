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
Code for handling HTML output formatting.
'''

# pylint:disable=R0903, R0801, W0237

import xml.etree.ElementTree as ET
from media.fmt.formatter.stream import AbstractStream


class HtmlStream(AbstractStream):
    '''
    The HTML stream is the string text output
    of the object data.

    NOTE: It probably shouldn't retain the element object.
    '''
    def __init__(self, in_element=None):
        super().__init__()
        self.mime_type = 'text/html'
        self.extension = 'html'
        self.element = None
        if in_element:
            self.element = in_element

    # We're violating W0237 here by changing a variable name.
    # If we were static typing, the type would also be
    # different
    def input(self, in_element=None):
        '''
        Input object to be sent out.
        '''
        if in_element is not None:
            self.element = in_element

    def __str__(self):
        ET.indent(self.element, space=' ')
        return ET.tostring(self.element,
                           encoding='us-ascii',
                           method='xml').decode('utf-8')

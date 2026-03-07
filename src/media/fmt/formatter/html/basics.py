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
HTML formatting for basic text structures.
'''

# pylint: disable=R0801, R0903

import xml.etree.ElementTree as ET
import media.fmt.structure.basics


class Basics():
    '''
    Basic rendering.
    '''

    def __init__(self):
        self.count = 0

    def render(self, in_object):
        '''
        Call the appropriate render function based
        on the passed object.
        '''
        out = ''
        if in_object:
            if issubclass(in_object.__class__,
                          media.fmt.structure.basics.Paragraph):
                out = Paragraph.render(in_object)
            elif issubclass(in_object.__class__,
                            media.fmt.structure.basics.Header):
                out = Header.render(in_object.text)
        return out


class Header():
    '''
    A header element.
    '''
    @classmethod
    def render(cls, in_object=None):
        '''
        Render the header.
        '''
        element = ET.Element('h1')
        if in_object:
            element.text = in_object.text
        return element


class Paragraph():
    '''
    A text paragraph.
    '''
    def __init__(self):
        self.count = 0

    @classmethod
    def render(cls, in_object=None):
        '''
        Render the paragraph.
        '''
        element = ET.Element('p')
        if in_object:
            element.text = in_object.text
        return element


class Line():
    '''
    A single line element.
    '''
    @classmethod
    def render(cls):
        '''
        Render the line.
        '''
        element = ET.Element('hr')
        return element

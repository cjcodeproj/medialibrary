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

'''
HTML formatting for basic text structures.
'''

# pylint: disable=R0801

import media.fmt.structure.basics


class Basics():
    '''
    Basic rendering.
    '''

    def render(self, in_object):
        '''
        Call the appropriate render function based
        on the passed object.
        '''
        out = ''
        if in_object:
            if issubclass(in_object.__class__,
                          media.fmt.structure.basics.Paragraph):
                out = self.render_para(in_object)
            elif issubclass(in_object.__class__,
                            media.fmt.structure.basics.Header):
                out = self.render_header(in_object)
        return out

    def render_para(self, in_structure):
        '''
        Render a paragraph.
        '''
        return f"\n<p>{in_structure!s}</p>\n"

    def render_header(self, in_structure):
        '''
        Render a header.
        '''
        return f"\n<h1>{in_structure!s}</h1>\n"

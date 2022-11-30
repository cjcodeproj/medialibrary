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

'''
Object classes related to the plot of a piece of
visual media.
'''

# pylint: disable=too-few-public-methods

import re
from media.xml.namespaces import Namespaces
from media.data.media.contents.generic.keywords import Keywords


class Story():
    '''
    The story is the main narrative of the film or other media.
    '''
    def __init__(self, in_element):
        self.plot = None
        self.keywords = None
        self.themes = []
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'plot':
                self.plot = Plot(child)
            if tagname == 'overview':
                self.plot = Plot(child)
            if tagname == 'keywords':
                self.keywords = Keywords(child)


class Plot():
    '''
    The plot is a written summary of the narrative.
    '''
    def __init__(self, in_element):
        self.plot = ""
        self._build(in_element)

    def _build(self, in_element):
        out = []
        if in_element.text:
            out.append(in_element.text.lstrip())
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'chr':
                out.append(child.text.lstrip())
            if tagname == 'kw':
                out.append(child.text.lstrip())
            if child.tail:
                out.append(child.tail)
        out_string = "".join(out)
        out_string = re.sub(r'\s+', ' ', out_string)
        self.plot = out_string

    def __str__(self):
        return self.plot

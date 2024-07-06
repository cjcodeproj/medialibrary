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

'''
Song object structure
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801

from media.data.media.contents.audio.elements import (
        AbstractElement, ElementTechnical
        )
from media.xml.namespaces import Namespaces


class Dialogue(AbstractElement):
    '''
    Object representation of a song.
    '''
    def __init__(self, in_element, in_parent):
        super().__init__()
        self.classification = None
        self.technical = None
        self.parent_o = in_parent
        self._process(in_element)

    def _process(self, in_element=None):
        super()._process(in_element)
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'technical':
                self.technical = ElementTechnical(child)

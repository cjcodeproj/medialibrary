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

'''Main module file for the Movie() and Title() objects'''

# pylint: disable=too-few-public-methods

from media.xml.namespaces import Namespaces

from media.data.media.library.instances import Instance
from media.data.media.library.filing import Filing


class Library():
    '''Library object - instance tracking and local filing info.'''
    def __init__(self, in_element):
        self.instances = []
        self.filing = None
        self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'instances':
                self._pull_instances(child)
            if child.tag == Namespaces.nsf('media') + 'filing':
                self.filing = Filing(child)

    def _pull_instances(self, in_element):
        for child in in_element:
            if child.tag == Namespaces.nsf('media') + 'instance':
                self.instances.append(Instance(child))

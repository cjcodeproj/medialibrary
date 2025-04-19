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
Abstract formatter class that all sublclasses inherit.
'''

# pylint: disable=R0903

import importlib


class AbstractFormatter():
    '''
    Abstract formatter class.
    '''

    structure_matrix = {}

    def __init__(self):
        self.rend_obj_pool = {}
        self.rend_count = {}

    def render(self, in_structure_obj):
        '''
        Launch a formatter object and return the output
        stream.
        '''
        output = ''
        rend_obj = self.get_renderer_for_structure(in_structure_obj)
        if rend_obj:
            output = rend_obj.render(in_structure_obj)
            self._counter_tally(rend_obj)
        return output

    def get_renderer_for_structure(self, in_object):
        '''
        Return a rendering object spefici to the structure object.
        '''
        struct_class = in_object.__class__
        if struct_class in self.structure_matrix:
            rend_class = self.structure_matrix[struct_class]
            if rend_class not in self.rend_obj_pool:
                rend_module = rend_class.__module__
                im_module = importlib.import_module(rend_module)
                rend_obj = getattr(im_module, rend_class.__name__)()
                self.rend_obj_pool[rend_class] = rend_obj
            return self.rend_obj_pool[rend_class]
        return None

    def _counter_tally(self, in_rend_obj):
        rend_class = in_rend_obj.__class__
        if rend_class in self.rend_count:
            self.rend_count[rend_class] += 1
        else:
            self.rend_count[rend_class] = 1

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
Code for handling the selection of an output formatter.
'''

# pylint:disable=R0903

import sys
import importlib


class Selector():
    '''
    Class for loading up the appropriate formatter
    code based on the output format requested.
    '''
    modules = {
            'html': 'media.fmt.formatter.html',
            'plaintext': 'media.fmt.formatter.plaintext',
            'csv': 'media.fmt.formatter.csv'
            }

    @classmethod
    def load_formatter(cls, in_driver):
        '''
        Loads a formatter object.
        '''
        drv = None
        if in_driver in Selector.modules:
            drv = importlib.import_module(Selector.modules[in_driver])
        else:
            print('DRIVER NOT LOADED')
        return getattr(sys.modules[drv.__name__], 'DriverMain')()

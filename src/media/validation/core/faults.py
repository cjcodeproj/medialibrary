#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
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
Objects pertaining to validation test faults.
'''

# pylint: disable=R0903


class FaultLevel():
    '''
    Fault levels.
    '''
    NOTICE = 1
    WARNING = 2
    CRITICAL = 3


class Fault():
    '''
    A fault is the equivelant of an exception
    when validating media records.
    '''
    def __init__(self, in_level, in_message, in_text=None):
        self.level = in_level
        self.message = in_message
        self.text = in_text

    def lvl_str(self):
        '''
        Return the fault level as a string.
        '''
        matrix = {
                  FaultLevel.NOTICE: 'NOTICE',
                  FaultLevel.WARNING: 'WARNING',
                  FaultLevel.CRITICAL: 'CRITICAL'
                 }
        return matrix[self.level]

    def __str__(self):
        if self.text:
            return f"{self.lvl_str()}: {self.message} ({self.text})"
        return f"{self.lvl_str()}: {self.message}"

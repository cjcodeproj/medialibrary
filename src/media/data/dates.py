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
Objects for representation of dates, either exact, or a date range.
'''

# pylint: disable=too-few-public-methods


class AbstractDate():
    '''
    Abstract class which has data shared by both
    child classes.
    '''
    def __init__(self):
        self.date = None


class ExactDate(AbstractDate):
    '''
    Representing an exact calendar date.
    '''
    def __init__(self, in_element):
        super().__init__()
        self.date = in_element.text

    def __str__(self):
        return f"{self.date}"


class RangeDate(AbstractDate):
    '''
    Representation for a non-specific date, where both an estimated start
    and an estimated end is known.  For example, if something was acquired
    in 2014, the start value would be 2014-01-01, and the end value would be
    P1Y, to allow coverage for every day in 2014.
    '''
    def __init__(self, in_element_1, in_element_2):
        super().__init__()
        self.date = in_element_1.text
        self.end = in_element_2.text

    def __str__(self):
        return f"{self.date} -> {self.end}"

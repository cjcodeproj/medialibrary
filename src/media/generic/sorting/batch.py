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

'''Grouping classes go here.'''

# pylint: disable=too-few-public-methods

import random


class AbstractBatch():
    '''
    A class containing contect objects all tied together
    by a common grouping factor.

    The index_key value is the sorting value for comparison
    between other batch values.

    The header value is the formal string for display purposes.

    The entries list is every item in the batch.
    '''
    S_TITLE = 'sort_title'
    S_YEAR = 'year'
    S_RUNTIME = 'runtime'
    S_ARTIST = 'artists'

    def __init__(self, index_key=None, header=None, first_entry=None):
        self.index_key = index_key
        self.header = header
        self.entries = []
        if first_entry:
            self.entries = [first_entry]

    def append(self, entry):
        '''
        Add a single entry to the end
        of the interal list.
        '''
        self.entries.append(entry)

    def extend(self, entries):
        '''
        Add a bunch of entries to the end
        of the interal list.
        '''
        self.entries.extend(entries)

    def index_by(self, attribute=S_TITLE):
        '''
        Return the batch items in order based
        on an attribute value within the object.
        '''
        order_list = []
        order_list = sorted(self.entries, key=lambda x:
                            getattr(x, attribute, ''))
        return order_list

    def random_entry(self):
        '''
        Return a single random entry from the batch.
        '''
        r_num = random.randint(0, len(self.entries)-1)
        return self.entries[r_num]

    def __lt__(self, other):
        return self.index_key < other.index_key

    def __rt__(self, other):
        return self.index_key > other.index_key

    def __eq__(self, other):
        return self.index_key == other.index_key


class Batch(AbstractBatch):
    '''
    An subclass of AbstractBatch, so
    the class AbstractBatch does not need to be
    instantiated.
    '''

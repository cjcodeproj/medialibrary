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

'''Common code related to content object sorting and grouping.'''

# pylint: disable=R0801
# pylint: disable=too-few-public-methods


import random
from media.generic.sorting.groups import (
        GroupAll, GroupTitleAlphabetical,
        GroupDecade, GroupPrimaryGenre)


class Organizer():
    '''
    Class that generates Batch objects based on content input.

    Batches are organized by title, year, or genre.

    If no Grouping parameter is presented, then all of
    the movies are put in a single batch.
    '''
    G_NONE = 0
    G_ALPHA = 1
    G_DECADE = 2
    G_GENRE = 3

    def __init__(self, in_list, sample_limit=None, grouping=None):
        self.batches = {}
        self.grouping = grouping
        self.entries = []
        self.original_count = len(in_list)
        if sample_limit:
            work_list = Organizer.get_random_sample(in_list, sample_limit)
        else:
            work_list = in_list
        if grouping:
            self.grouping = grouping
        else:
            self.grouping = Organizer.G_NONE
        self._build_entry_objects(work_list)
        self.sample_count = len(work_list)
        self._build_batches()

    @classmethod
    def get_random_sample(cls, in_list, limit):
        '''
        Take a large list, and turn it into a random sample.

        Find the total number of objects in the list.
        If the sample limit is greater than the number
        of objects, than just return the original list.

        Otherwise, generate a 'limit' number of random
        numbers, between 0 and the list total and put them
        in an array.  Then iterate through that array, using
        each random number as an index value against the
        original list.
        '''
        total = len(in_list)-1
        if limit > total:
            return in_list
        slots = []
        out = []
        while len(slots) <= limit-1:
            r_num = random.randint(0, total)
            if r_num not in slots:
                slots.append(r_num)
        for slot_i in slots:
            out.append(in_list[slot_i])
        return out

    def _build_entry_objects(self, in_list):
        for content_i in in_list:
            self.entries.append(content_i.build_index_object())

    def _build_batches(self):
        if self.grouping == Organizer.G_NONE:
            self.batches = GroupAll.group(self.entries)
        elif self.grouping == Organizer.G_ALPHA:
            self.batches = GroupTitleAlphabetical.group(self.entries)
        elif self.grouping == Organizer.G_DECADE:
            self.batches = GroupDecade.group(self.entries)
        elif self.grouping == Organizer.G_GENRE:
            self.batches = GroupPrimaryGenre.group(self.entries)

    def get_batches(self):
        """
        Return all of the batches that were created.
        """
        return list(self.batches.values())


GroupingOptions = {
        'none': Organizer.G_NONE,
        'alphabetical': Organizer.G_ALPHA,
        'decade': Organizer.G_DECADE,
        'genre': Organizer.G_GENRE
}


class ContentIndex():
    '''
    Abstract root class for all content index objects.
    '''
    def __init__(self):
        self.sort_title = None

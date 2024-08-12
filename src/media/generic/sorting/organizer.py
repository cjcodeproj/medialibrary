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

'''Common code related to content object sorting and grouping.'''

# pylint: disable=R0801
# pylint: disable=too-few-public-methods


import random
from media.generic.sorting.groups import (
        GroupAll, GroupTitleAlphabetical,
        GroupDecade, GroupPrimaryGenre)


class AbstractOrganizer():
    '''
    The AbstractOrganizer class takes a list of content objects and creates
    an output list of one or more batch objects, which contain the same
    content, collated in a desired structure.  IE, for a list of 30
    movies, the class will examine each movie, and divide it into
    batches based on criteria like the first letter of the title,
    the genre, or the decade it was made.

    This is an abstract class not meant to be instantiated.  Subclasses
    can add additional organization criteria.
    '''
    G_NONE = 1
    G_ANY_ALPHA = 2
    G_ANY_DECADE = 3
    G_ANY_GENRE = 4

    def __init__(self, in_list, grouping=None):
        self.batches = {}
        self.grouping = grouping
        self.entries = []
        self.working = []
        self.original_count = len(in_list)
        self._add_index_objects(in_list)
        if self.grouping is not None:
            self.grouping = AbstractOrganizer.G_NONE

    def _add_index_objects(self, in_list):
        for con in in_list:
            self.entries.append(con.s_index)

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

    def set_grouping(self, in_group):
        '''
        Set the grouping attribute value.
        '''
        self.grouping = in_group

    def create_batches(self, grouping=None, sample_limit=None):
        '''
        Create the Batch objects.
        '''
        if grouping:
            self.grouping = grouping
        if sample_limit:
            self.working = AbstractOrganizer.get_random_sample(self.entries,
                                                            sample_limit)
        else:
            self.working = self.entries
        self._build_batches()
        return list(self.batches.values())

    def _build_batches(self):
        if self.grouping == AbstractOrganizer.G_NONE:
            self.batches = GroupAll.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_ALPHA:
            self.batches = GroupTitleAlphabetical.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_DECADE:
            self.batches = GroupDecade.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_GENRE:
            self.batches = GroupPrimaryGenre.group(self.working)
        else:
            self.batches = GroupAll.group(self.working)
            print('group parameter did not match')


class Organizer(AbstractOrganizer):
    '''
    Direct subclass of AbstractOrganizer, with no
    additions or changes, meant to be used as the
    default organizer choice.  Use this class if
    there is no additional organiztion criteria.
    '''

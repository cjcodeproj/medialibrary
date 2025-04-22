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


from media.generic.sorting.groups import (
        Grouping, GroupAll, GroupTitleAlphabetical,
        GroupDecade, GroupPrimaryGenre)
from media.generic.sorting.batch import Batch
from media.generic.sorting.organizer import AbstractOrganizer


class AlbumOrganizer(AbstractOrganizer):
    '''
    DOCO
    '''
    G_ARTIST = 10

    def _build_batches(self):
        if self.grouping == AbstractOrganizer.G_NONE:
            self.batches = GroupAll.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_ALPHA:
            self.batches = GroupTitleAlphabetical.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_DECADE:
            self.batches = GroupDecade.group(self.working)
        elif self.grouping == AbstractOrganizer.G_ANY_GENRE:
            self.batches = GroupPrimaryGenre.group(self.working)
        elif self.grouping == AlbumOrganizer.G_ARTIST:
            self.batches = GroupArtist.group(self.working)
        else:
            self.batches = GroupAll.group(self.working)
            print('group parameter did not match')


class GroupArtist(Grouping):
    '''
    Group entries based on the artist name.
    '''
    @classmethod
    def group(cls, entries):
        '''
        Return multiple batches, grouped by album artist.
        '''
        groups = {}
        for con_ind in entries:
            if con_ind.artists not in groups:
                groups[con_ind.artists] = Batch(con_ind.artists.sort_string,
                                                con_ind.artists.formal_string,
                                                con_ind)
            else:
                groups[con_ind.artists].append(con_ind)
        return groups

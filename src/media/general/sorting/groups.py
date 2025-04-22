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

'''Grouping classes go here.'''

# pylint: disable=too-few-public-methods

from media.general.sorting.batch import Batch


class Grouping():
    '''
    Abstract class for grouping operations.
    '''
    @classmethod
    def group(cls, entries):
        """
        Group incoming entries based on a certain trait.
        """
        _ = entries
        return {}


class GroupAll(Grouping):
    '''
    Return a single set with all objects.
    '''
    @classmethod
    def group(cls, entries):
        """
        Return a single Batch with every entry in it.
        """
        groups = {}
        groups['all'] = Batch()
        groups['all'].extend(entries)
        return groups


class GroupTitleAlphabetical(Grouping):
    '''
    Grouping entries based on their title.
    '''
    @classmethod
    def group(cls, entries):
        """
        Return multiple batches, grouped by the
        first letter in the title.
        """
        groups = {}
        for con_ind in entries:
            if con_ind.first_letter not in groups:
                f_letter = con_ind.first_letter.upper()
                groups[con_ind.first_letter] = Batch(con_ind.first_letter,
                                                     f_letter, con_ind)
            else:
                groups[con_ind.first_letter].append(con_ind)
        return groups


class GroupDecade(Grouping):
    '''
    Grouping entries based on the decade they were created.
    '''
    @classmethod
    def group(cls, entries):
        """
        Return multiple batches, grouped by
        the decade of the copyright year.
        """
        groups = {}
        for con_ind in entries:
            if con_ind.decade not in groups:
                f_decade = str(con_ind.decade) + "0s"
                groups[con_ind.decade] = Batch(con_ind.decade,
                                               f_decade, con_ind)
            else:
                groups[con_ind.decade].append(con_ind)
        return groups


class GroupPrimaryGenre(Grouping):
    '''
    Grouping entries based on their primary genre.
    '''
    @classmethod
    def group(cls, entries):
        """
        Return multiple batches, grouped by
        the primary genre of the content.
        """
        groups = {}
        for con_ind in entries:
            if con_ind.primary_g not in groups:
                groups[con_ind.primary_g] = Batch(con_ind.primary_g,
                                                  con_ind.primary_g, con_ind)
            else:
                groups[con_ind.primary_g].append(con_ind)
        return groups

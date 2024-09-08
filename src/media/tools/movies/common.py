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

'''
Shared classes and subroutines for the list and show
modules.
'''


# pylint: disable=too-few-public-methods


import argparse
import os
import media.fmt.text.movie
from media.generic.sorting.organizer import Organizer
from media.generic.sorting.batch import Batch

CliGroupingOptions = {
        'none': Organizer.G_NONE,
        'alphabetical': Organizer.G_ANY_ALPHA,
        'decade': Organizer.G_ANY_DECADE,
        'genre': Organizer.G_ANY_GENRE,
}


CliSortOptions = {
        'title': Batch.S_TITLE,
        'year': Batch.S_YEAR,
        'runtime': Batch.S_RUNTIME,
}


class Controller():
    '''
    The Controller class manages aspects of the command
    execution.  It processes all of the CLI arguments,
    and tests file paths to make sure they exist.
    '''
    def __init__(self):
        self.args = None
        self.mediapath = None

    def setup(self):
        '''
        Initialize the command line parser, and make sure
        the mediapath exists.
        '''
        parser = self._setup_parser()
        self.args = parser.parse_args()
        self._determine_path()

    def _setup_parser(self):
        '''
        Set up the parser object.
        '''
        parser = argparse.ArgumentParser(description='Album list')
        parser.add_argument('--mediapath', help='path of media repository')
        parser.add_argument('--random', type=int,
                            help='print X random entries')
        parser.add_argument('--group',
                            choices=['none', 'alphabetical',
                                     'decade',
                                     'genre'],
                            help='Album grouping',
                            default='none')
        parser.add_argument('--sort',
                            choices=['title', 'year', 'runtime'],
                            help='Album sorting',
                            default='title')
        parser.add_argument('--stats',
                            action=argparse.BooleanOptionalAction,
                            help='Report statistics')
        return parser

    def _determine_path(self):
        '''
        Verify that the media path with the XML files exists.
        '''
        mediapath = self.args.mediapath
        if not mediapath:
            if 'MEDIAPATH' in os.environ:
                mediapath = os.environ['MEDIAPATH']
        self.mediapath = mediapath


class MovieReport():
    '''
    Class that does all the listing work.

    Accepts a list of movies as input,
    and generates a report output as a string.

    Should also be directly callable from
    an interactive Python prompt.
    '''
    def __init__(self):
        self.organizer = None
        self.movies = []
        self.sample = 0
        self.group = Organizer.G_ANY_ALPHA
        self.asort = Batch.S_TITLE
        self.stats = False

    def set_movies(self, in_movies, in_controller=None):
        '''
        Pass all the Album content objects that were
        found in the repository.
        '''
        if len(in_movies) > 0:
            self.movies = in_movies
            self.organizer = Organizer(in_movies)
            if in_controller:
                self.params_from_controller(in_controller)

    def params_from_controller(self, in_controller):
        '''
        Get the parameters from the controller object.
        '''
        self.group = CliGroupingOptions[in_controller.args.group]
        self.asort = CliSortOptions[in_controller.args.sort]
        if in_controller.args.random:
            self.sample = in_controller.args.random
        if in_controller.args.stats:
            self.stats = True

    def report(self, grouping=None, sorting=None, sample=0, stats=False):
        '''
        1. Output the headers.
        2. Count the batches
        '''
        if grouping:
            self.group = grouping
        if sorting:
            self.asort = sorting
        if self.sample == 0:
            self.sample = max(sample, 0)
        if stats:
            self.stats = stats
        out = ''
        out += media.fmt.text.movie.OneLiner.header_fields()
        self.organizer.set_grouping(self.group)
        if self.sample > 0:
            batches = self.organizer.create_batches(self.group, self.sample)
        else:
            batches = self.organizer.create_batches(self.group)
        if len(batches) == 1:
            out += self._out_batch(batches[0], self.asort)
        else:
            for batch_i in sorted(batches):
                out += f"  -- {batch_i.header} ({len(batch_i.entries)}) --\n"
                out += self._out_batch(batch_i, self.asort)
        out = out[:-1]
        out += media.fmt.text.movie.OneLiner.header_line()
        if self.stats:
            out += self._stats()
        return out

    def _stats(self):
        '''
        Output the basic stats on the number of movies,
        and the number of movies in the sample set
        (if one is defined)
        '''
        all_c = len(self.organizer.entries)
        wrk_c = len(self.organizer.working)
        out = f"  {'Movie count':12s} : {all_c:5d}\n"
        if wrk_c < all_c:
            wrk_p = float(wrk_c) / all_c * 100
            out += f"  {'Sample count':12s} : {wrk_c:5d} ({wrk_p:5.2f}%)\n"
        return out

    def _out_batch(self, batch, sort_field=1):
        '''
        Generate the output for a single batch.
        '''
        out = ''
        order_list = batch.index_by(sort_field)
        for movie in order_list:
            out += str(media.fmt.text.movie.OneLiner(movie.movie))
        out += "\n"
        return out

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

"""
Simple command to output details on every movie.
"""

# pylint: disable=R0801
# pylint: disable=too-few-public-methods

# brief movie report
import argparse
import media.fmt.text.movie
from media.fileops.filenames import FilenameMatches
from media.fileops.repo import Repo
from media.tools.movies.common import (Controller,
                                       MovieReport)


class ShowController(Controller):
    '''
    Subclass of default Controller class.
    '''
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
        parser.add_argument('--pagebreaks',
                            action=argparse.BooleanOptionalAction,
                            help='Page breaks on output')
        parser.add_argument('--stats',
                            action=argparse.BooleanOptionalAction,
                            help='Report statistics')
        return parser


class MovieShowReport(MovieReport):
    '''
    Subclass of MovieReport class.
    '''
    def __init__(self):
        super().__init__()
        self.pagebreaks = False

    def params_from_controller(self, in_controller):
        super().params_from_controller(in_controller)
        if in_controller.args.pagebreaks:
            self.pagebreaks = True

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
        # out += media.fmt.text.movie.OneLiner.header_fields()
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
        # out += media.fmt.text.movie.OneLiner.header_line()
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
        out = "\n    ---- Movie Statistics ----\n\n"
        out += f"  {'Movie count':12s} : {all_c:5d}\n"
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
            out += str(media.fmt.text.movie.Brief(movie.movie))
            out += "\n"
            if self.pagebreaks:
                out += chr(12)
        return out


def main_cli():
    '''
    Entry point for script.

    Steps:
      1. Argument parsing/environment setup
      2. Repository loading
      3. Batch processing
      4. Listing
    '''
    controller = ShowController()
    controller.setup()

    repo = Repo(controller.mediapath)
    repo.scan()
    repo.load(FilenameMatches.All_Media)
    movies = repo.get_movies()
    movie_report = MovieShowReport()
    movie_report.set_movies(movies)
    movie_report.params_from_controller(controller)
    print(movie_report.report())


if __name__ == '__main__':
    main_cli()

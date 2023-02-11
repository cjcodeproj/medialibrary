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

"""
Simple command to output details on every movie.
"""

# pylint: disable=R0801

# brief movie report
import os
import argparse
import media.fmt.text.movie
from media.generic.sorting.groups import (BatchSortOptions)
from media.generic.sorting.lists import (GroupingOptions, Organizer)
from media.tools.common import (load_movies)


def show_movie_batches(incoming, sort_field=1, page_breaks=False):
    """
    Iterate through every batch and report on the movie.
    """
    if len(incoming) == 1:
        show_batch(incoming[0], sort_field, page_breaks)
    else:
        for batch_i in sorted(incoming):
            print(f"{'-' * 40}")
            print(f"-- {batch_i.header} ({len(batch_i.entries)}) --")
            print(f"{'-' * 40}\n")
            show_batch(batch_i, sort_field, page_breaks)


def show_batch(batch, sort_field=1, page_breaks=False):
    """
    Iterate through every movie in a batch and report.
    """
    order_list = batch.index_by(sort_field)
    for movie in order_list:
        print(media.fmt.text.movie.Brief(movie.movie))
        if page_breaks:
            print(chr(12))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    parser.add_argument('--group',
                        choices=['none', 'alphabetical', 'decade', 'genre'],
                        help='Grouping field',
                        default='none')
    parser.add_argument('--sort',
                        choices=['title', 'year', 'runtime'],
                        help='Sort field',
                        default='title')
    parser.add_argument('--pagebreaks', action=argparse.BooleanOptionalAction,
                        help='Page break after every movie.')
    args = parser.parse_args()
    moviepath = args.mediapath or os.environ['MEDIAPATH']
    if not moviepath:
        parser.print_help()
    all_movies = load_movies(moviepath)
    organizer = Organizer(all_movies,
                          args.random,
                          grouping=GroupingOptions[args.group])
    batches = organizer.get_batches()
    show_movie_batches(batches, BatchSortOptions[args.sort], args.pagebreaks)

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
List out all movies (or a random sample of all movies),
one entry per line.
"""

# pylint: disable=R0801

import os
import argparse
import media.fmt.text.movie
from media.generic.sorting.groups import (BatchSortOptions)
from media.generic.sorting.lists import (GroupingOptions, Organizer)
from media.tools.common import (load_movies)


def list_movie_batches(incoming, sort_field=1):
    """
    Iterate through every batch and report on the movie
    inside the batch.
    """
    print(media.fmt.text.movie.OneLiner.header_fields())
    if len(incoming) == 1:
        list_batch(incoming[0], sort_field)
    else:
        for batch_i in sorted(incoming):
            print(f"\n -- {batch_i.header} ({len(batch_i.entries)}) --\n")
            list_batch(batch_i, sort_field)
    print(media.fmt.text.movie.OneLiner.header_line())


def list_batch(batch, sort_field=1):
    """
    Iterate through every movie in a single batch.
    """
    order_list = batch.index_by(sort_field)
    for movie in order_list:
        print(media.fmt.text.movie.OneLiner(movie.movie))


def report_stats(org):
    """
    Report statistics on the data presented.
    """
    print(f"  Movie count : {org.original_count:5d}")
    if org.sample_count < org.original_count:
        c_percent = float(org.sample_count) / \
                    org.original_count * 100
        print(f"  Sample size : {org.sample_count:5d}  " +
              f"({c_percent:5.2f}%)")


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
    parser.add_argument('--stats',
                        action=argparse.BooleanOptionalAction,
                        help='Report statistics')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    all_movies = load_movies(mediapath)
    organizer = Organizer(all_movies,
                          args.random,
                          grouping=GroupingOptions[args.group])
    batches = organizer.get_batches()
    list_movie_batches(batches, BatchSortOptions[args.sort])
    if args.stats:
        report_stats(organizer)

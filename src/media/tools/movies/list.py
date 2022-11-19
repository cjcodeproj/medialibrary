#!/usr/bin/env python
"""
List out all movies (or a random sample of all movies),
one apiece per line.
"""

# pylint: disable=R0801

import os
import argparse
import media.fmt.text.movie
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


def list_movies(in_list, sort_field=None):
    '''
    Provide a summary list of all movies, sorted by title or runtime.
    '''
    if sort_field == 'runtime':
        order_list = sorted(in_list, key=lambda x: x.runtime)
    else:
        order_list = sorted(in_list, key=lambda x: x.title_key)
    print(media.fmt.text.movie.List.list_header())
    for movie_out in order_list:
        print(movie_out)
    print(media.fmt.text.movie.List.list_header_line())


def prep_list(in_movies):
    '''
    Build the list of output entries.
    '''
    out_l = []
    for movie in in_movies:
        out_l.append(media.fmt.text.movie.List(movie))
    return out_l


def report_stats(in_full, in_sample):
    """
    Report on the data collected.
    """
    a_c = len(in_full)
    s_c = len(in_sample)
    print(f"  Movie count : {a_c:5d}")
    if s_c < a_c:
        c_percent = float(s_c) / a_c * 100
        print(f"  Sample size : {s_c:5d}  ({c_percent:5.2f}%)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    parser.add_argument('--sort', choices=['title', 'runtime'],
                        help='Sort field')
    parser.add_argument('--stats',
                        action=argparse.BooleanOptionalAction,
                        help='Report statistics')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    if args.random:
        sample = prep_list(random_sample_list(all_movies, args.random))
    else:
        sample = prep_list(all_movies)
    if args.sort:
        list_movies(sample, args.sort)
    else:
        list_movies(sample)
    if args.stats:
        report_stats(all_movies, sample)

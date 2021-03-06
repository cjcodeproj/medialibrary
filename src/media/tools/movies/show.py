#!/usr/bin/env python
'''Simple command line client to list out movies'''

# pylint: disable=R0801

# brief movie report
import os
import argparse
import media.fmt.text.movie
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


def show_movies(in_list, sort_field=None):
    '''
    Show every movie entry, ordered by either title or runtime.
    '''
    if sort_field == 'runtime':
        order_list = sorted(in_list, key=lambda x: x.runtime)
    else:
        order_list = sorted(in_list, key=lambda x: x.title_key)
    for movie_out in order_list:
        print(movie_out)


def prep_list(in_movies):
    '''
    Build the list of output entries.
    '''
    out_l = []
    for movie in in_movies:
        out_l.append(media.fmt.text.movie.Brief(movie))
    return out_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    parser.add_argument('--sort', choices=['title', 'runtime'],
                        help='Sort field')
    args = parser.parse_args()
    moviepath = args.mediapath or os.environ['MEDIAPATH']
    if not moviepath:
        parser.print_help()
    devices = load_media_dev(moviepath)
    all_movies = compile_movies(devices)
    if args.random:
        chunks = prep_list(random_sample_list(all_movies, args.random))
    else:
        chunks = prep_list(all_movies)
    if args.sort:
        show_movies(chunks, args.sort)
    else:
        show_movies(chunks)

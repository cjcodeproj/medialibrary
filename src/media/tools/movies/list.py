#!/usr/bin/env python
'''
List out all movies, one per line.
'''

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


def prep_list(in_movies):
    '''
    Build the list of output entries.
    '''
    out_l = []
    for movie in in_movies:
        out_l.append(media.fmt.text.movie.List(movie))
    return out_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    parser.add_argument('--sort', choices=['title', 'runtime'],
                        help='Sort field')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    if args.random:
        chunks = prep_list(random_sample_list(all_movies, args.random))
    else:
        chunks = prep_list(all_movies)
    if args.sort:
        list_movies(chunks, args.sort)
    else:
        list_movies(chunks)

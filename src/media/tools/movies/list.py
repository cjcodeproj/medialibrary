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


def list_movies(movies):
    '''Provide a summary list of all movies'''
    print(media.fmt.text.movie.List.list_header())
    for movie in sorted(movies):
        movie_list_entry = media.fmt.text.movie.List(movie)
        print(movie_list_entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    if args.random:
        rand_limit = args.random
        list_movies(random_sample_list(all_movies, rand_limit))
    else:
        list_movies(all_movies)

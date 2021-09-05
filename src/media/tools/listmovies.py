#!/usr/bin/env python
'''
List out all movies, one per line.
'''

# pylint: disable=R0801

import os
import argparse
import media.fmt.text.movie
from media.tools.common import load_media_dev


def list_movies(media_devices):
    '''Provide a summary list of all movies'''
    print(media.fmt.text.movie.List.list_header())
    for m_dev in media_devices:
        for movie in m_dev.contents:
            movie_list_entry = media.fmt.text.movie.List(movie)
            print(movie_list_entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    list_movies(devices)

#!/usr/bin/env python
'''Simple command line client to list out movies'''

# pylint: disable=R0801

# brief movie report
import os
import argparse
import media.fmt.text.movie
from media.tools.common import load_media_dev


def print_movies(media_devices):
    '''Do a brief report on the movies'''
    for m_dev in media_devices:
        for movie in m_dev.contents:
            movie_record = media.fmt.text.movie.Brief(movie)
            print(movie_record)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    moviepath = args.mediapath or os.environ['MEDIAPATH']
    if not moviepath:
        parser.print_help()
    devices = load_media_dev(moviepath)
    print_movies(devices)

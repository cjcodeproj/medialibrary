#!/usr/bin/env python
'''
List out all movies, one per line.
'''

# pylint: disable=R0801

import os
import argparse
import media.fmt.text.media
from media.tools.common import (
        load_media_dev, random_sample_list
        )


def list_devices(in_list):
    '''
    Provide a summary list of all movies, sorted by title or runtime.
    '''
    print(media.fmt.text.media.ListEntry.header())
    ordered_list = sorted(in_list, key=lambda x: x.title_key)
    for movie_out in ordered_list:
        print(movie_out)


def prep_list(in_movies):
    '''
    Build the list of output entries.
    '''
    out_l = []
    for media_i in in_movies:
        out_l.append(media.fmt.text.media.ListEntry(media_i))
    return out_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple media list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    args = parser.parse_args()

    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    if args.random:
        chunks = prep_list(random_sample_list(devices, args.random))
    else:
        chunks = prep_list(devices)
    list_devices(chunks)

#!/usr/bin/env python

#
# Copyright 2022 Chris Josephes
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

'''
List out all physical media, one per line.
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

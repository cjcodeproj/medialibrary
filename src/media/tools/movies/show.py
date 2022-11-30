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

'''Simple command line client to list out movies'''

# pylint: disable=R0801

# brief movie report
import os
import argparse
import media.fmt.text.movie
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


def show_movies(in_list, in_args):
    '''
    Show every movie entry, ordered by either title or runtime.
    '''
    sort_field = in_args.sort
    p_breaks = in_args.pagebreaks
    if sort_field == 'runtime':
        order_list = sorted(in_list, key=lambda x: x.runtime)
    else:
        order_list = sorted(in_list, key=lambda x: x.title_key)
    for movie_out in order_list:
        print(movie_out)
        if p_breaks:
            print(chr(12))


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
    parser.add_argument('--pagebreaks', action=argparse.BooleanOptionalAction,
                        help='Page break after every movie.')
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
    show_movies(chunks, args)

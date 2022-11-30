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
Module to report on all keywords within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


class KeywordTitleMap():
    '''
    One keyword object with a list of titles that utilize that keyword.


    '''
    def __init__(self, in_keyword, in_title):
        self.keyword = in_keyword
        self.titles = [in_title]

    def add_title(self, in_title):
        '''Add a movie title to an existing keyword object.'''
        self.titles.append(in_title)

    @classmethod
    def header(cls):
        '''Print a simple header.'''
        out = f"{'Keyword':45s} {'Title'}\n" + \
              f"{'=' * 45} {'=' * 25}\n"
        return out

    def __str__(self):
        '''Print out the keyword with a sorted title list'''
        out = ''
        line = 1
        for title_i in sorted(self.titles):
            if line == 1:
                out += f"{self.keyword.detail():45s} {title_i!s}\n"
            else:
                out += f"{' ':45s} {title_i!s}\n"
            line += 1
        return out

    def __lt__(self, other):
        return self.keyword.sort_value < other.keyword.sort_value

    def __gt__(self, other):
        return self.keyword.sort_value > other.keyword.sort_value

    def __eq__(self, other):
        return self.keyword.sort_value == self.keyword.sort_value


def grab_keywords(movies):
    '''
    Build a dictionary of all keywords.

    For every movie, pull all of the keywords.

    For existing keywords in the dictionary, add the title to
    the existing object.
    '''
    kw_dict = {}
    for movie in movies:
        kw_pull = None
        story = None
        if movie.story is not None:
            story = movie.story
        elif movie.description is not None:
            story = movie.description
        if story.keywords is not None:
            kw_pull = story.keywords.all()
            for kw_i in kw_pull:
                kw_detail = kw_i.detail()
                if kw_detail in kw_dict:
                    kw_dict[kw_detail].add_title(movie.title)
                else:
                    kw_dict[kw_detail] = \
                            KeywordTitleMap(kw_i, movie.title)
    return list(kw_dict.values())


def list_keywords(keywords):
    '''Print the keywords that are passed along.'''
    print(KeywordTitleMap.header(), end='')
    for kw_i in sorted(keywords):
        print(kw_i, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='show X keywords')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    all_keywords = grab_keywords(all_movies)
    if args.random:
        rand_limit = args.random
        list_keywords(random_sample_list(all_keywords, rand_limit))
    else:
        list_keywords(all_keywords)

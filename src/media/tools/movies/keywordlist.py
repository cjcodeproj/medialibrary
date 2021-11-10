#!/usr/bin/env python
'''
Module to report on all named within a movie
'''

# pylint: disable=R0801
# pylint: disable=too-few-public-methods

import os
import argparse
from media.tools.common import load_media_dev, compile_movies


class KWP():
    '''
    KWP (KeywordPair)

    Simple class to associate keywords to movie titles

    This could be really inefficient POC code
    '''

    def __init__(self, keyword, title):
        self.keyword = keyword
        self.title = title


class KeywordList():
    '''Build a structure of keywords and titles'''
    def __init__(self):
        self.kwo = {}

    def add(self, keyword, title):
        '''Add a name, job role, and title to the list'''
        if keyword.sort_value in self.kwo:
            self.kwo[keyword.sort_value].append(KWP(keyword, title))
        else:
            self.kwo[keyword.sort_value] = [KWP(keyword, title)]

    def output(self):
        '''Return the keywords and titles'''
        print(f"{'Keyword':45s} {'Title'}")
        print(f"{'=' * 45} {'=' * 25}")
        for kwd in sorted(self.kwo.keys()):
            t_count = 1
            for keyword_obj in self.kwo[kwd]:
                if t_count == 1:
                    print(f"{keyword_obj.keyword.detail():45s} " +
                          f"{keyword_obj.title!s}")
                else:
                    print(f"{' ':45s} {keyword_obj.title!s}")
                t_count += 1


def grab_keywords(movies):
    '''Extract keywords from a movie'''
    kw_list = KeywordList()
    kw_src = None
    for movie in movies:
        if movie.story is not None:
            if movie.story.keywords is not None:
                kw_src = movie.story.keywords.all()
        elif movie.description is not None:
            if movie.description.keywords is not None:
                kw_src = movie.description.keywords.all()
        if kw_src is not None:
            for keyword in kw_src:
                kw_list.add(keyword, movie.title)
    return kw_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    names = grab_keywords(all_movies)
    names.output()

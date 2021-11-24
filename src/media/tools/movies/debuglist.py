#!/usr/bin/env python
'''
List out all movies, one per line.
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import load_media_dev, compile_movies


class DebugList():
    '''Formatting a listing of movies, one per line.'''
    def __init__(self, in_movie):
        self.movie = in_movie
        self.output = ""
        self.output += self.mentry()

    @classmethod
    def list_header(cls):
        '''Generate a simple header'''
        out = f"{'Title':35s} {'Year':4s} "
        out += f"{'Hash':20s} {'Object Address':18s}\n"
        out += f"{'=' * 35} {'=' * 4} {'=' * 20} {'=' * 18}"
        return out

    def mentry(self):
        '''One line entry'''
        y_string = ""
        if self.movie.catalog is not None:
            if self.movie.catalog.copyright is not None:
                y_string = self.movie.catalog.copyright.year
        hash_string = hash(self.movie)
        out = f"{self.movie.title!s:35s} {y_string:4d} "
        out += f"{hash_string:20d} {hex(id(self.movie))}"
        return out

    def __str__(self):
        return self.output


def list_movies(movies):
    '''Provide a summary list of all movies'''
    table = {}
    print(DebugList.list_header())
    for movie in sorted(movies):
        movie_list_entry = DebugList(movie)
        print(movie_list_entry)
        if movie not in table:
            table[movie] = True
    print(f"Unique movie count: {len(table.keys())}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    list_movies(all_movies)

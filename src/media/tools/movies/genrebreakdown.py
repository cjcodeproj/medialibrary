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
List out all movie genres, grouped by primary and secondary genres.
'''

# pylint: disable=R0801

import os
import argparse
import random
from media.tools.common import load_media_dev, compile_movies


class PrimaryBucket():
    '''
    Bucket class system for primary genres.

    Very simple dictionary where key values are the primary genre name, and
    the value is a list containing the movie objects.
    '''
    def __init__(self):
        self.genres = {}
        self.movie_count = 0

    def add(self, genre, movie):
        '''
        Add a movie to a genre, regardless of whether it exists or not.
        '''
        if genre in self.genres:
            self.genres[genre].append(movie)
        else:
            self.genres[genre] = [movie]
        self.movie_count += 1

    def bucket(self, genre):
        '''
        Return the list for a specific genre.
        '''
        if genre in self.genres:
            return self.genres[genre]
        return None

    def report(self):
        '''
        Generate a primary genre report.
        '''
        out = f"{' ' * 55} {'<<< Primary Genres >>>'}\n\n"
        out += f"{'Primary Genre':15s} {'Count':5s} {'Perc':6s} " + \
               f"{'Ratio':50s} {'Sample Title'}\n"
        out += f"{'-' * 15}  {'-' * 5} {'-' * 6} {'-' * 50} {'-' *45}\n"
        for genre in sorted(self.genres):
            pg_tally = len(self.genres[genre])
            perc = float(pg_tally / self.movie_count * 100)
            text_pro_bar = proportion_bar(pg_tally, self.movie_count)
            rand_movie = random_movie(self.bucket(genre))
            out += f"{genre:15s}  {pg_tally:5d} {perc:5.1f}% " + \
                   f"{text_pro_bar:50s} {rand_movie.title!s}\n"
        out += f"{'-' * 15}  {'-' * 5} {'-' * 6} {'-' * 50} {'-' *45}\n"
        out += f"Total movie count {self.movie_count}\n\n"
        return out


class SecondaryBucket():
    '''
    A class for a primary/secondary bucket tree.

    A slightly more complex dictionary compared to PrimaryBucket.
    Each key is still based on the value of 'primary', but the value is another
    dictionary, with each key of the smaller dictionary being the values of
    the 'secondary' elements, and the value being a list of movie objects.
    '''
    def __init__(self):
        self.genres = {}
        self.movie_count = 0

    def add(self, in_primary, in_secondaries, movie):
        '''
        Populate the primary/secondary buckets.
        '''
        if len(in_secondaries) == 0:
            self._add_no_secondaries(in_primary, movie)
        else:
            self._add_with_secondaries(in_primary, in_secondaries, movie)
        self.movie_count += 1

    def _add_no_secondaries(self, in_primary, movie):
        '''
        Add a movie to a special secondary bucket signifying
        that there are no secondary genres for this movie.
        '''
        sec_genre = '(none)'
        if in_primary in self.genres:
            if sec_genre in self.genres[in_primary]:
                self.genres[in_primary][sec_genre].append(movie)
            else:
                self.genres[in_primary][sec_genre] = [movie]
        else:
            self.genres[in_primary] = {sec_genre: [movie]}

    def _add_with_secondaries(self, in_primary, in_secondaries, movie):
        '''
        Add a movie to every possible secondary genre bucket
        for a given primary genre bucket.
        '''
        for sec_genre in in_secondaries:
            if in_primary in self.genres:
                if sec_genre in self.genres[in_primary]:
                    self.genres[in_primary][sec_genre].append(movie)
                else:
                    self.genres[in_primary][sec_genre] = [movie]
            else:
                self.genres[in_primary] = {sec_genre: [movie]}

    def _count_primary_unique(self, in_primary):
        '''
        We need this to count movies under a primary genre
        that may fall into multiple secondary buckets.

        This function creates a list and iterates through
        all of the movies, but only adds the movie object to
        the list if it isn't already present.
        '''
        out = []
        for secondary_i in self.genres[in_primary]:
            for movie in self.genres[in_primary][secondary_i]:
                if movie not in out:
                    out.append(movie)
        return len(out)

    def _count_secondary_occurences(self, in_primary_g):
        sec_occur = 0
        for prim_g in self.genres:
            for sec_g in self.genres[prim_g]:
                if sec_g == in_primary_g:
                    # sec_occur += 1
                    sec_occur += len(self.genres[prim_g][sec_g])
        return sec_occur

    def bucket(self, in_primary, in_secondary):
        '''
        Quick routine to get to a specific bucket.
        '''
        if in_primary in self.genres:
            if in_secondary in self.genres[in_primary]:
                return self.genres[in_primary][in_secondary]
        return None

    def report(self):
        '''
        Generate a secondary genre report.
        '''
        out = f"{' ' * 54} {'<<< Secondary Genres >>>'}\n\n"
        for primary_i in sorted(self.genres):
            sec_tally = 0
            for secondary_i in self.genres[primary_i]:
                sec_tally += len(self.genres[primary_i][secondary_i])
            prim_count = self._count_primary_unique(primary_i)
            sec_occur = self._count_secondary_occurences(primary_i)
            out += f"\nPrimary Genre: {primary_i:12s}  ({prim_count:d} / " + \
                   f"{self.movie_count:d}) "
            out += f"Occurences as a secondary genre: {sec_occur}\n\n"
            out += f"{'Secondary Genre':12s} {'Count':5s} {'Perc':6s} " + \
                   f"{'Ratio':50s} {'Sample Title'}\n"
            out += f"{'-' * 15} {'-' * 5} {'-' * 6} {'-' * 50} {'-' * 45}\n"
            for secondary_i in sorted(self.genres[primary_i]):
                sec_count = len(self.genres[primary_i][secondary_i])
                perc = float(sec_count / sec_tally * 100)
                text_pro_bar = proportion_bar(sec_count, sec_tally)
                rand_movie = random_movie(self.genres[primary_i][secondary_i])
                out += f"{secondary_i:15s} {sec_count:5d} {perc:5.1f}% " + \
                       f"{text_pro_bar:50s} {rand_movie.title!s}\n"
            out += f"{'-' * 15} {'-' * 5} {'-' * 6} {'-' * 50} {'-' * 45}\n"
        return out


def report_header():
    '''
    Print a simplified report header.
    '''
    out = f"{'=' * 132}\n\n"
    out += f" {'Movie Genre Report'}\n\n"
    out += f"{'=' * 132}\n\n"
    return out


def populate_primary_buckets(movies):
    '''Put the primary genre of every movie in a bucket.'''
    pg_bucket = PrimaryBucket()
    for movie in movies:
        if movie.classification.genres:
            prim_genre = movie.classification.genres.primary
            pg_bucket.add(prim_genre, movie)
    return pg_bucket


def populate_secondary_buckets(movies):
    '''Put the primary and secondary genres of every movie in a bucket.'''
    sg_bucket = SecondaryBucket()
    for movie in movies:
        if movie.classification.genres:
            prim_genre = movie.classification.genres.primary
            sec_genre = movie.classification.genres.secondary
            sg_bucket.add(prim_genre, sec_genre, movie)
    return sg_bucket


def proportion_bar(value, maximum, limit=50):
    '''
    Generate a proportional text bar based on a set of values, including
    the desired value, the maximum possible value, and the
    character limit on how long the bar can be.
    '''
    ratio = int(value / maximum * limit)
    tics = ratio * '-'
    return f"{tics}"


def random_movie(in_list):
    '''
    For a given list of movies, return one random
    movie from the list.
    '''
    total_count = len(in_list)
    if total_count == 1:
        random_index = 0
    else:
        random_index = random.randint(0, len(in_list)-1)
    return in_list[random_index]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    primary = populate_primary_buckets(all_movies)
    secondary = populate_secondary_buckets(all_movies)
    print(report_header())
    print(primary.report())
    print(secondary.report())

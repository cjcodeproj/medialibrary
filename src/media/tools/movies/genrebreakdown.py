#!/usr/bin/env python
'''
List out all movies, one per line.
'''

# pylint: disable=R0801

import os
import argparse
import random
from media.tools.common import load_media_dev, compile_movies


class PrimaryBucket():
    '''
    Bucket class system for primary genres.
    '''
    def __init__(self):
        self.genres = {}
        self.movie_count = 0

    def add(self, genre, title):
        '''
        Add a title to a genre, regardless of whether it exists or not.
        '''
        if genre in self.genres:
            self.genres[genre].append(title)
        else:
            self.genres[genre] = [title]
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
            rand_title = random_title(self.bucket(genre))
            out += f"{genre:15s}  {pg_tally:5d} {perc:5.1f}% " + \
                   f"{text_pro_bar:50s} {rand_title}\n"
        out += f"{'-' * 15}  {'-' * 5} {'-' * 6} {'-' * 50} {'-' *45}\n"
        out += f"Total movie count {self.movie_count}\n\n"
        return out


class SecondaryBucket():
    '''
    A class for a primary/secondary bucket tree.
    '''
    def __init__(self):
        self.genres = {}
        self.movie_count = 0

    def add(self, in_primary, in_secondaries, title):
        '''
        Populate the primary/secondary buckets.
        '''
        if len(in_secondaries) == 0:
            self._add_no_secondaries(in_primary, title)
        else:
            self._add_with_secondaries(in_primary, in_secondaries, title)
        self.movie_count += 1

    def _add_no_secondaries(self, in_primary, title):
        '''
        Add a movie to a special secondary bucket signifying
        that there are no secondary genres for this movie.
        '''
        sec_genre = '(none)'
        if in_primary in self.genres:
            if sec_genre in self.genres[in_primary]:
                self.genres[in_primary][sec_genre].append(title)
            else:
                self.genres[in_primary][sec_genre] = [title]
        else:
            self.genres[in_primary] = {sec_genre: [title]}

    def _add_with_secondaries(self, in_primary, in_secondaries, title):
        '''
        Add a movie to every possible secondary genre bucket
        for a given primary genre bucket.
        '''
        for sec_genre in in_secondaries:
            if in_primary in self.genres:
                if sec_genre in self.genres[in_primary]:
                    self.genres[in_primary][sec_genre].append(title)
                else:
                    self.genres[in_primary][sec_genre] = [title]
            else:
                self.genres[in_primary] = {sec_genre: [title]}

    def _count_primary_unique(self, in_primary):
        '''
        We need this to count movies under a primary genre
        that may fall into multiple secondary buckets.
        '''
        out = []
        for secondary_i in self.genres[in_primary]:
            for title in self.genres[in_primary][secondary_i]:
                if title not in out:
                    out.append(title)
        return len(out)

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
            out += f"\nPrimary Genre: {primary_i}  ({prim_count} / " + \
                   f"{self.movie_count})\n\n"
            out += f"{'Secondary Genre':15s} {'Count':5s} {'Perc':6s} " + \
                   f"{'Ratio':50s} {'Sample Title'}\n"
            out += f"{'-' * 15} {'-' * 5} {'-' * 6} {'-' * 50} {'-' * 45}\n"
            for secondary_i in sorted(self.genres[primary_i]):
                sec_count = len(self.genres[primary_i][secondary_i])
                perc = float(sec_count / sec_tally * 100)
                text_pro_bar = proportion_bar(sec_count, sec_tally)
                rand_title = random_title(self.genres[primary_i][secondary_i])
                out += f"{secondary_i:15s} {sec_count:5d} {perc:5.1f}% " + \
                       f"{text_pro_bar:50s} {rand_title}\n"
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
            pg_bucket.add(prim_genre, movie.title)
    return pg_bucket


def populate_secondary_buckets(movies):
    '''Put the primary and secondary genres of every movie in a bucket.'''
    sg_bucket = SecondaryBucket()
    for movie in movies:
        if movie.classification.genres:
            prim_genre = movie.classification.genres.primary
            sec_genre = movie.classification.genres.secondary
            sg_bucket.add(prim_genre, sec_genre, movie.title)
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


def random_title(in_list):
    '''
    For a given list of movie titles, return one random
    title from the list.
    '''
    total_count = len(in_list)
    if total_count == 1:
        random_index = 0
    else:
        random_index = random.randint(0, len(in_list)-1)
    return str(in_list[random_index])


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

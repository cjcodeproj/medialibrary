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
Module to report on all named within a movie
'''

# pylint: disable=R0801

import os
import argparse
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


class ActorRoleMap():
    '''
    Align an actor with all of their roles
    '''
    def __init__(self, in_role, in_movie):
        self.name = in_role.actor
        self.movies = {}
        self.movies[in_movie] = in_role.portrays

    def add_movie(self, in_role, in_movie):
        '''
        Add movie object and role data to the entry.
        '''
        if in_movie in self.movies:
            self.movies[in_movie].extend(in_role.portrays)
        else:
            self.movies[in_movie] = in_role.portrays

    def movie_count(self):
        """
        Return a count of movies for a given actor.
        """
        return len(self.movies.keys())

    def get_movies(self):
        """
        Return all the movie objects for a given actor.
        """
        return self.movies.keys()

    @classmethod
    def header(cls):
        '''
        Generate a report header
        '''
        out = f"{'Actor Name':30s} {'Title':30s} {'Portrays':30s}\n" + \
              cls.header_line()
        return out

    @classmethod
    def header_line(cls):
        """
        Return a header line.
        """
        return f"{'=' * 30} {'=' * 30} {'=' * 30}\n"

    def __str__(self):
        out = ''
        name_c = 1
        for movie in sorted(self.movies):
            title_c = 1
            for portrays in self.movies[movie]:
                if name_c == 1:
                    out += f"{self.name!s:30s} {movie.title!s:30s} " + \
                           f"{portrays.formal!s:30s}\n"
                else:
                    if title_c == 1:
                        out += f"{' ':30s} {movie.title!s:30s} " + \
                               f"{portrays.formal!s:30s}\n"
                    else:
                        out += f"{' ':30s} {' ':30s} {portrays.formal!s:30s}\n"
                name_c += 1
                title_c += 1
        return out

    def __lt__(self, other):
        return self.name < other.name

    def __rt__(self, other):
        return self.name > other.name

    def __eq__(self, other):
        return self.name == other.name


def grab_cast_names(in_movies):
    '''
    Extract cast names from movies.
    '''
    ca_dict = {}
    for movie in in_movies:
        if movie.crew is not None:
            if movie.crew.cast:
                for role in movie.crew.cast.cast:
                    if role.actor in ca_dict:
                        ca_dict[role.actor].add_movie(role, movie)
                    else:
                        ca_dict[role.actor] = ActorRoleMap(role, movie)
    return list(ca_dict.values())


def find_empty_movies(in_movies):
    """
    Identify movies that have no cast.
    """
    ca_list = []
    for movie in in_movies:
        if movie.crew:
            if not movie.crew.cast:
                ca_list.append(movie)
        else:
            ca_list.append(movie)
    return ca_list


def list_names(in_names):
    '''
    Output all of the passed names.
    '''
    print(ActorRoleMap.header(), end='')
    for nm_i in sorted(in_names):
        print(nm_i, end='')
    print(ActorRoleMap.header_line(), end='')


def report_stats(in_names, in_sample):
    """
    Report stats on data, whether it's all actors
    or a random sample.
    """
    all_n = stats_compile(in_names)
    partial_n = None
    if len(in_sample) < len(in_names):
        partial_n = stats_compile(in_sample)
    print()
    if partial_n:
        report_stats_sample(all_n, partial_n)
    else:
        report_stats_all(all_n)


def report_stats_all(all_n):
    """
    Formatted output when no random sub-sample
    of actor data was requested.
    """
    print(f"{' ':29s} {'Entire Set'}")
    print(f"{' ':29s} {'-' * 10}")
    print(f"{'Actor count:':29s} {all_n['names']:10d}")
    print(f"{'Movie count:':29s} {all_n['movies']:10d}")
    print(f"{'Average movies per actor:':29s} {all_n['act_mov_avg']:10.2f}")


def report_stats_sample(all_n, partial_n):
    """
    Formatted output when a ransom sub-sample
    of actor data was requested.
    """
    print(f"{' ':29s} {'Entire Set'} {'Sample Set'} {'Percentage'}")
    print(f"{' ':29s} {'-' * 10} {'-' * 10} {'-' * 10}")
    n_p = float(partial_n['names']) / all_n['names'] * 100
    m_p = float(partial_n['movies']) / all_n['movies'] * 100
    print(f"{'Actor count:':29s} " +
          f"{all_n['names']:>10d} " +
          f"{partial_n['names']:>10d} {n_p:9.2f}%")
    print(f"{'Movie count:':29s} " +
          f"{all_n['movies']:>10d} " +
          f"{partial_n['movies']:>10d} {m_p:9.2f}%")
    print(f"{'Average movies per actor:':29s} " +
          f"{all_n['act_mov_avg']:10.2f} " +
          f"{partial_n['act_mov_avg']:10.2f}")


def stats_compile(in_names):
    """
    Basic statistics on actors and films.
    A total count of the number of actors.
    A total count of the number of movies with actors.
    An average of how many acting jobs fo0r each
    actor given the sample of movies.
    """
    out_d = {}
    out_d['names'] = len(in_names)
    movies_from_actors = {}
    for act_i in in_names:
        for movie_i in act_i.movies:
            if movie_i in movies_from_actors:
                movies_from_actors[movie_i] += 1
            else:
                movies_from_actors[movie_i] = 1
    out_d['movies'] = len(movies_from_actors.keys())
    act_mov_tot = 0
    for act_i in in_names:
        act_mov_tot += act_i.movie_count()
    out_d['act_mov_avg'] = float(act_mov_tot) / out_d['names']
    return out_d


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='show X names')
    parser.add_argument('--stats', action=argparse.BooleanOptionalAction,
                        help='Report statistics')
    parser.add_argument('--report-empty',
                        action=argparse.BooleanOptionalAction,
                        dest='report_empty',
                        help='Report movies with no cast')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    names = grab_cast_names(all_movies)
    empty = find_empty_movies(all_movies)
    if len(empty) > 0 and args.report_empty:
        print(f"{len(empty)} movies have no cast")
        for mi in empty:
            print(f"{str(mi.title)}")
    if args.random:
        rand_limit = args.random
        sample_names = random_sample_list(names, rand_limit)
    else:
        sample_names = names
    list_names(sample_names)
    if args.stats:
        report_stats(names, sample_names)

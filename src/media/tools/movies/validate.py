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
Run simple validation tests against the movies, report any incomplete data.
'''

# pylint: disable=R0801
# pylint: disable=too-few-public-methods

import os
import argparse
from datetime import timedelta
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )


class Status():
    '''
    Status object for a given movie.

    It contains the movie object, an array of faults,
    and a simple flag determining whether or not the
    film is acceptable.
    '''
    def __init__(self, in_movie):
        self.movie = in_movie
        self.acceptable = True
        self.faults = []

    def add_fault(self, in_fault):
        '''Add a fault object to the movie status'''
        self.faults.append(in_fault)
        self.acceptable = False

    def report_faults(self):
        '''Report faults for a movie if present.'''
        out = ''
        if not self.acceptable:
            fault1 = self.faults.pop(0)
            out = f"{self.movie.title!s:50s} {fault1!s}\n"
            for flt in self.faults:
                out += f"{' ' * 50} {flt!s}\n"
        return out

    @classmethod
    def status_header(cls):
        '''Return a generic output header.'''
        return f"{'Movie Title':50s} {'Faults'}\n" + \
               f"{'-' * 50:s} {'-' * 25:s}"

    def __lt__(self, other):
        return self.movie.unique_key < other.movie.unique_key

    def __gt__(self, other):
        return self.movie.unique_key > other.movie.unique_key


class Fault():
    '''
    Fault class, identifying the reason for the fault, and
    a severity score.
    '''
    def __init__(self, in_reason, in_score=5):
        self.reason = in_reason
        self.score = in_score

    def __str__(self):
        return self.reason


class Tester():
    '''
    Simple tester class that examines the attributes of a movie,
    and identifies faults if they are present.
    '''

    @classmethod
    def test_plot(cls, movie_status):
        '''Test the movie plot.'''
        p_string = str(movie_status.movie.story.plot).strip()
        if not p_string:
            movie_status.add_fault(Fault("Plot missing"))
        else:
            words = p_string.split()
            pwc = len(words)
            if pwc < 20:
                movie_status.add_fault(Fault("Plot has less than 20 words"))

    @classmethod
    def test_technical(cls, movie_status):
        '''Test the movie technical data.'''
        if movie_status.movie.technical:
            tech = movie_status.movie.technical
            if tech.runtime:
                runtime = tech.runtime.overall or timedelta(0)
                if runtime == timedelta(0):
                    movie_status.add_fault(Fault("Runtime is undefined"))
                elif runtime == timedelta(seconds=1, minutes=1, hours=1):
                    movie_status.add_fault(Fault("Suspicious runtime value"))
        else:
            movie_status.add_fault(Fault("Technical block missing"))

    @classmethod
    def test_catalog(cls, movie_status):
        '''Test the movie catalog data.'''
        if movie_status.movie.catalog:
            mcat = movie_status.movie.catalog
            if mcat.copyright:
                if len(mcat.copyright.holders) == 0:
                    movie_status.add_fault(Fault("No copyright holder info"))
            else:
                movie_status.add_fault(Fault("No copyright info"))


def validate_movies(in_list):
    '''
    Initialize all the movie status objects, and then
    run through the tests.
    '''
    m_status = []
    for movie in in_list:
        m_status.append(Status(movie))
    for movie_s in m_status:
        Tester.test_plot(movie_s)
        Tester.test_technical(movie_s)
        Tester.test_catalog(movie_s)
    return m_status


def report_validation(in_list):
    '''
    Report any movie faults if they are present.
    '''
    print(Status.status_header())
    for movie_s in sorted(in_list):
        if not movie_s.acceptable:
            print(movie_s.report_faults(), end='\r')


def report_stats(all_movies_c, sample_c, in_reports):
    '''
    Provide a summary report on all movie faults.
    '''
    fault_count = 0
    for report_i in in_reports:
        if not report_i.acceptable:
            fault_count += 1
    print(f"{'-' * 50} {'-' * 25}")
    print(f"{'Movie Count :':>25s} {all_movies_c}")
    print(f"{'Random Sample Size :':>25s} {sample_c} " +
          f"({sample_c/all_movies_c*100:5.2f}%)")
    print(f"{'Fault Count :':>25s} {fault_count}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--random', type=int, help='print X random entries')
    parser.add_argument('--stats', action='store_true',
                        help='report statistics')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    if args.random:
        sample = random_sample_list(all_movies, args.random)
    else:
        sample = all_movies
    status_reports = validate_movies(sample)
    report_validation(status_reports)
    if args.stats:
        report_stats(len(all_movies), len(sample), status_reports)

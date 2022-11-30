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
List out a breakdown of movie time lengths into buckets.
'''

# pylint: disable=R0801

from datetime import timedelta

import os
import argparse
from media.tools.common import (
        load_media_dev, compile_movies, random_sample_list
        )
from media.tools.movies.list import prep_list
from media.tools.movies.genrebreakdown import proportion_bar


class BucketManager():
    '''
    Holds all bucket objects, and performs
    reporting, and data aggregation operations across all of them.
    '''
    def __init__(self, in_limit=10):
        self.limit = in_limit
        self.buckets = []
        self.average = None
        self.median = None
        self.median_title = ''
        self.movie_count = 0
        self.interval = 0

    def initialize_bucket_ranges(self, in_list):
        '''
        Set up ever bucket object (up to limit), and
        configure the range values of each object.
        '''
        shortest = in_list[0].runtime
        longest = in_list[-1].runtime
        interval = self.get_bucket_interval(shortest, longest)
        # print(f"Interval is {interval}\n")
        start_i = shortest
        for _ in range(1, self.limit + 1):
            self.buckets.append(Bucket(start_i, interval, len(in_list)))
            start_i += timedelta(seconds=interval)

    def get_bucket_interval(self, shortest, longest):
        '''
        Determine the bucket interval length by subtracting the shortest
        movie runtime from the longest movie runtime, then divide it
        by the number of requested buckets.  This requires turning the
        runtimes into integers that represent all of the seconds in the
        timedelta object.

        Input is two timedelta objects, and the return value is another
        timedelta object.
        '''
        delta_range = longest - shortest
        delta_int = int(delta_range.total_seconds())
        range_int = int(delta_int / self.limit) + 1
        self.interval = timedelta(seconds=range_int)
        return range_int

    def install_in_buckets(self, in_list):
        '''
        For every passed movie, install it into a bucket by
        passing it to every bucket object, knowing that
        it only gets accepted into a single bucket.

        There are probably ways to make this code more
        efficient.
        '''
        total_r = 0
        for movie_i in in_list:
            for bucket_i in self.buckets:
                if bucket_i.is_in_range(movie_i.runtime):
                    bucket_i.movies.append(movie_i)
                    break
            total_r += movie_i.runtime.total_seconds()
        self.movie_count = len(in_list)
        self.calculate_average(total_r)
        self.calculate_median(in_list)

    def calculate_average(self, total_runtimes):
        '''
        Caculate the average time of all the movies.
        '''
        average_seconds = int(total_runtimes / self.movie_count)
        self.average = timedelta(seconds=average_seconds)

    def calculate_median(self, in_list):
        '''
        Calculate the median time of all the movies, and
        report on which titles(s) fit the median.
        '''
        if self.movie_count % 2 == 0:
            median1 = int(self.movie_count / 2)
            median2 = median1 + 1
            total_median_seconds = in_list[median1].runtime.total_seconds() + \
                in_list[median2].runtime.total_seconds()
            self.median = timedelta(seconds=int(total_median_seconds / 2))
            self.median_title = f"{in_list[median1].movie.title!s:s} / " + \
                f"{in_list[median2].movie.title!s:s}"
        else:
            median1 = int(self.movie_count / 2)
            self.median = in_list[median1].runtime
            self.median_title = f"{in_list[median1].movie.title!s:s}"

    def report_buckets(self):
        '''
        Generate a report on all buckets, by sending the report command
        to every bucket in the list.  Then provide summary data
        at the bottom of the report.
        '''
        print(Bucket.header())
        for bucket_i in self.buckets:
            print(bucket_i.report())
        print(Bucket.hdr_lines())
        print(f"         Movie count : {self.movie_count}")
        print(f"Average film runtime : {self.average!s:s}")
        print(f" Median film runtime : {self.median!s:8s} " +
              f"({self.median_title})")
        print(f"     Interval Length : {self.interval!s:s}")
        print(f"        Bucket Count : {len(self.buckets)}")


class Bucket():
    '''
    A single bucket designed to hold movie objects.

    It has a low end limit and a high end limit, and then uses those
    timedelta values to see if a movie should go in that bucket
    based on the length of the movie.
    '''
    def __init__(self, in_low_limit, in_range,  in_total_count):
        self.low_limit = in_low_limit
        self.high_limit = in_low_limit + timedelta(seconds=in_range)
        self.total_count = in_total_count
        self.movies = []

    def is_in_range(self, in_timedelta):
        '''
        Simple check to see if a passed movie falls within the bucket
        range.
        '''
        return bool(self.low_limit <= in_timedelta < self.high_limit)

    def range_print(self):
        '''
        A debugging method to examine the bucket status.
        '''
        return f"Low   : {self.low_limit}\n" + \
            f"High  : {self.high_limit}\n" + \
            f"Count : {len(self.movies)} / {self.total_count}\n\n"

    @classmethod
    def header(cls):
        '''
        Sends out a report header.
        '''
        out = f"{'Random Title':50s} " + \
              f"{'From':8s} {'To':8s} " + \
              f"{'Count':5s} {'Perc':6s} {'Ratio':50s}\n" + \
              cls.hdr_lines()
        return out

    @classmethod
    def hdr_lines(cls):
        '''
        Sends out formatting lines used in the report header.
        '''
        return f"{'-' * 50} {'-'*8} {'-'*8} {'-'*5} {'-'*6} {'-'*50}"

    def report(self):
        '''
        Generate a report entry on a single bucket object.
        Show the range limits (low and high, the number of
        movies, the percentage based on a total, and a tick bar
        for illustrative purposes.  Also show a random movie title.
        '''
        tick_bar = proportion_bar(len(self.movies), self.total_count)
        movie = random_sample_list(self.movies, 1)
        if len(movie) > 0:
            mov_title = str(movie[0].movie.title)
            perc = float(len(self.movies) / self.total_count * 100)
        else:
            mov_title = " << None >>"
            perc = 0
        return f"{str(mov_title):50s} {self.low_limit!s:>8s} " + \
               f"{self.high_limit!s:>8s} {len(self.movies):5d} " + \
               f"{perc:5.1f}% {tick_bar}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath', help='path of media library')
    parser.add_argument('--buckets', type=int, help='number of sample buckets')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    all_movies = compile_movies(devices)
    list_entries = prep_list(all_movies)
    sorted_movies = sorted(list_entries, key=lambda x: x.runtime)
    if args.buckets:
        buckets = BucketManager(args.buckets)
    else:
        buckets = BucketManager()
    buckets.initialize_bucket_ranges(sorted_movies)
    buckets.install_in_buckets(sorted_movies)
    buckets.report_buckets()

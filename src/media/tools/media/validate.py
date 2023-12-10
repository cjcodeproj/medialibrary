#!/usr/bin/env python

#
# Copyright 2023 Chris Josephes
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

import argparse
import os
from datetime import datetime
from media.data.media.medium.release import FormalType
from media.generic.sorting.lists import Organizer
from media.tools.common import load_media_dev

from media.validation.core.validator import Validator
from media.validation.core.status import Tally


def filter_output_set(in_results, in_args):
    '''
    Output a random sample of records.
    '''
    outset = []
    # final = []
    for result in in_results:
        if in_args.filter == 'none':
            outset.append(result)
        elif in_args.filter == 'passing':
            if result.has_passed():
                outset.append(result)
        else:
            if not result.has_passed():
                outset.append(result)
    if in_args.random:
        # return random_sample(output, args.random)
        return Organizer.get_random_sample(outset, in_args.random)
    return outset


def output_list(filtered_list):
    '''
    Output a simple list of results.
    '''
    print(Tally.header(), end='')
    for sample_i in filtered_list:
        mtype = FormalType.formal_convert(sample_i.media.medium.release.type)
        status_o = sample_i.status
        print(f"{sample_i.media!s:40.39s} {mtype:10s} {status_o.tally!s}")


def output_details(filtered_list):
    '''
    Output the full status report of every piece of media.
    '''
    for sample_i in filtered_list:
        print(sample_i.status.report())


def output_timestamp(in_start_time):
    '''
    Output program run timestamp data.
    '''
    end_time = datetime.now()
    out = f"\n {'Program Start Time'} : {in_start_time}\n" + \
          f"   {'Program End Time'} : {end_time}\n" + \
          f"         {'Duration'}   : {end_time - start_time}\n"
    return out


def single_column_stats(in_results):
    '''
    Output a single column of stats.
    '''
    output = "\n"
    all_passed = 0
    all_failed = 0
    all_total = len(in_results)
    for result in in_results:
        if result.has_passed():
            all_passed += 1
        else:
            all_failed += 1
    all_perc = all_passed / all_total * 100
    output += f"{' ':20s} {'Entire Set'}\n" + \
              f"{' ':20s} {'-'*10}\n" + \
              f"{'Total Media:':20s} {all_total:10d}\n" + \
              f"{'Perfect:':20s} {all_passed:10d}\n" + \
              f"{'Failed:':20s} {all_failed:10d}\n\n" + \
              f"{'Overall Percentage:':20s} {all_perc:9.2f}%\n"
    return output


def double_column_stats(in_results, in_filtered_results):
    '''
    Output two columns of stats, comparing all results
    and the filtered results.
    '''
    output = "\n"
    all_total = len(in_results)
    sample_total = len(in_filtered_results)
    all_passed = 0
    all_failed = 0
    sample_passed = 0
    sample_failed = 0
    for result in in_results:
        if result.has_passed():
            all_passed += 1
        else:
            all_failed += 1
    for result in in_filtered_results:
        if result.has_passed():
            sample_passed += 1
        else:
            sample_failed += 1
    all_perc = all_passed / all_total * 100
    sample_perc = sample_passed / sample_total * 100
    output += f"{' ':20s} {'Entire Set'} {'Sample Set'}\n" + \
              f"{' ':20s} {'-'*10} {'-'*10}\n" + \
              f"{'Total Media:':20s} {all_total:10d} {sample_total:10d}\n" + \
              f"{'Passed:':20s} {all_passed:10d} {sample_passed:10d}\n" + \
              f"{'Failed:':20s} {all_failed:10d} {sample_failed:10d}\n\n" + \
              f"{'Overall Percentage:':20s} {all_perc:9.2f}% " +\
              f"{sample_perc:9.2f}%\n"
    return output


def output_stats(in_start_time, in_results, in_filtered):
    '''
    Output overall statistics, including time metrics.
    '''
    o_total = len(results)
    f_total = len(filtered_results)
    output = ''
    if f_total == o_total:
        output = single_column_stats(in_results)
    else:
        output = double_column_stats(results, in_filtered)
    output += output_timestamp(in_start_time)
    print(output)


if __name__ == '__main__':
    start_time = datetime.now()
    parser = argparse.ArgumentParser(description='Simple movie list.')
    parser.add_argument('--mediapath',
                        help='path of media library')
    parser.add_argument('--level',
                        type=int,
                        default=4,
                        choices=range(1, 6),
                        help='diagnostic level')
    parser.add_argument('--filter',
                        choices=['passing', 'failed', 'none'],
                        default='none',
                        help='records to output')
    parser.add_argument('--random', type=int, help='show X random entries')
    parser.add_argument('--list',
                        action=argparse.BooleanOptionalAction,
                        default=True,
                        help='list records')
    parser.add_argument('--details',
                        action=argparse.BooleanOptionalAction,
                        default=False,
                        help='show record details')
    parser.add_argument('--stats', action='store_true',
                        help='report statistics')
    args = parser.parse_args()
    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    media = load_media_dev(mediapath)
    sample = media
    validator = Validator()
    validator.set_suite()
    validator.load_media(sample, args.level)
    results = validator.run_tests()
    if args.filter:
        filtered_results = filter_output_set(results, args)
    else:
        filtered_results = results
    if args.list:
        output_list(filtered_results)
    if args.details:
        output_details(filtered_results)
    if args.stats:
        output_stats(start_time, results, filtered_results)

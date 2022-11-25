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
Code to handle technical aspects of a vidsual format media
(movies, television)
'''

# pylint: disable=too-few-public-methods

import re
from datetime import timedelta
from media.xml.namespaces import Namespaces


class Technical():
    '''
    Technical element block.

    Covering visual format, palette, and runtime.
    '''
    def __init__(self, in_element):
        self.runtime = None
        self.palette = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'runtime':
                self.runtime = Runtime(child)


class Runtime():
    '''
    Class for handling the runtime interval of a movie or TV show.
    '''
    def __init__(self, in_element):
        self.overall = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            tagname = Namespaces.ns_strip(child.tag)
            if tagname == 'overall':
                dur_string = child.text
                dur_value = process_iso_duration(dur_string)
                self.overall = dur_value


def process_iso_duration(in_string):
    '''
    Process an ISO duration value

    Ex: like P01H20M37S (1 hour, 20 minutes, 37 seconds)
    '''
    duration_regex = r"PT(?P<hours>\d{1,2}H)?(?P<minutes>\d{1,2}M)?" +\
                     r"(?P<seconds>\d{1,2}S)?"
    dur_match = re.match(duration_regex, in_string)
    if dur_match is not None:
        if dur_match.group('hours') is not None:
            in_hours = int(dur_match.group('hours').rstrip('H'))
        else:
            in_hours = 0
        if dur_match.group('minutes') is not None:
            in_minutes = int(dur_match.group('minutes').rstrip('M'))
        else:
            in_minutes = 0
        if dur_match.group('seconds') is not None:
            in_seconds = int(dur_match.group('seconds').rstrip('S'))
        else:
            in_seconds = 0
        return timedelta(hours=in_hours,
                         minutes=in_minutes,
                         seconds=in_seconds)
    return None

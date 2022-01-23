#!/usr/bin/env python
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
        in_hours = int(dur_match.group('hours').rstrip('H') or '0')
        in_minutes = int(dur_match.group('minutes').rstrip('M') or '0')
        in_seconds = int(dur_match.group('seconds').rstrip('S') or '0')
        return timedelta(hours=in_hours,
                         minutes=in_minutes,
                         seconds=in_seconds)
    return None

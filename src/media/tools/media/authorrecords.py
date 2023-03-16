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
List out all physical media, one per line.
'''

# pylint: disable=R0801

import os
import argparse
import media.data.media.meta.authorship as MA
from media.tools.common import (
        load_media_dev
        )


def list_authorship_recs(in_list):
    '''
    Provide a summary list of all movies, sorted by title or runtime.
    '''
    for record_i in in_list:
        title = record_i.title
        a_string = ''
        if record_i.catalog.authors:
            for a_name in record_i.catalog.authors:
                a_string += a_name.name + " "
            a_string = a_string[:-1]
        print(f"{title:40s} ({a_string})")
        if record_i.changelog:
            for c_rec in record_i.changelog:
                if issubclass(c_rec.__class__, MA.CreationRecord):
                    print('-' * 50)
                    print(f"Created: {c_rec.tstamp!s}")
        print()


def prep_list(in_devices):
    '''
    Build the list of output entries.
    '''
    out_l = []
    for media_i in in_devices:
        if media_i.author_record:
            out_l.append(media_i.author_record)
    return out_l


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple media list.')
    parser.add_argument('--mediapath', help='path of media library')
    args = parser.parse_args()

    mediapath = args.mediapath or os.environ['MEDIAPATH']
    if not mediapath:
        parser.print_help()
    devices = load_media_dev(mediapath)
    chunks = prep_list(devices)
    list_authorship_recs(chunks)

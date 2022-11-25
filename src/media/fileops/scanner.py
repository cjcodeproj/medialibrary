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
Code to scan one or more directories for media files
'''

# media.scanner

import os.path
import time
from os import listdir
from os.path import isdir, isfile


class Walker():
    '''Scans directory for media XML files'''
    def __init__(self, in_paths, debug=False):
        self.dirs = []
        self.files = []
        self.skipped = []
        self.elapsed = None
        self.match_re = None
        self.debug = debug
        self.dirs.append(in_paths[0])

    def filename_match(self, in_match):
        '''Pass filename matching regex'''
        self.match_re = in_match

    def scan(self):
        '''Scan the directory tree for files'''
        tstart = time.time()
        for s_dir in self.dirs:
            for s_file in listdir(s_dir):
                full_path = os.path.join(s_dir, s_file)
                if self.debug:
                    print(f"{s_dir!s} {s_file!s} {full_path!s}")
                if isdir(full_path):
                    if not s_file.startswith('.'):
                        self.dirs.append(full_path)
                elif isfile(full_path):
                    self.files.append(full_path)
        tend = time.time()
        self.elapsed = tend - tstart

    def name_match(self, in_filename):
        '''Test a filename to ensure it matches our search pattern'''
        if self.match_re:
            if self.match_re.search(in_filename):
                return True
        return False

    def stats(self):
        '''Simple statistical output'''
        return f"{len(self.dirs)} {len(self.files)} {len(self.skipped)}"

    def report(self):
        '''More detailed report of scanner operations'''
        out = "Stats\n-----\n"
        out += f"Directory Count   : {len(self.dirs)}\n"
        out += f"File Count        : {len(self.files) + len(self.skipped)}\n"
        out += f"        Matched   : {len(self.files)}\n"
        out += f"    Non-Matched   : {len(self.skipped)}\n"
        out += f"Elapsed Time      : {self.elapsed:02f}\n"
        return out

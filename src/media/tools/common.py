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

'''Common routines for command line tools'''

# pylint disable=R0801

import media.fileops.scanner
import media.fileops.loader
import media.fileops.repo
from media.fileops.filenames import FilenameMatches

# Walker module walks the filesystem
# Loader module reads in the discovered files


def load_media_dev(in_path):
    '''Identify suitable files and load them up'''
    repo = media.fileops.repo.Repo(in_path)
    repo.scan()
    repo.load(FilenameMatches.Movie_Media)
    return repo.media


def load_movies(in_path):
    '''
    Load all files that are tied to movie media devices.
    '''
    repo = media.fileops.repo.Repo(in_path)
    repo.scan()
    repo.load(FilenameMatches.Movie_Media)
    return repo.get_movies()

#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
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
Object representation of a medialibrary file repository.

The object is a representation of all files under a directory tree.
The first method call is always to scan() to identify all directories
and files, which persist int he object memory.

It contains an object that does the actual scanning work
(which can be swapped out), and an object to do the loading
and creation of the media objects.
'''

from media.data.media.contents.movie import Movie
from media.data.media.contents.audio.album import Album
from media.fileops.loader import Loader
from media.fileops.scanner import Walker


class Repo():
    '''
    The repository object.
    '''
    def __init__(self, in_path):
        self.root_path = in_path
        self.walker = Walker([in_path])
        self.dirs = []
        self.files = []
        self.media = []
        self.content = []

    def set_walker(self, in_object):
        '''
        For the rare occasion when someone wants to swap out the default
        walker object.
        '''
        self.walker = in_object

    def scan(self):
        '''
        Have the walker object scan the repo path.
        '''
        self.walker.scan()
        self.dirs = self.walker.dirs
        self.files = self.walker.files

    def file_match(self, in_pattern):
        '''
        Return all filenames matching a specific pattern.
        '''
        out = []
        for fname in self.files:
            if in_pattern.search(fname):
                out.append(fname)
        return out

    def load(self, pattern=None):
        '''
        Load all media files and generate the media objects.
        '''
        loader = Loader()
        self.media = loader.load_media(self, pattern)
        self._extract_content()

    def _extract_content(self):
        for m_dev in self.media:
            for con_obj in m_dev.contents:
                if con_obj not in self.content:
                    self.content.append(con_obj)

    def get_movies(self):
        '''
        Extract all content objects that are the Movie class.
        '''
        out = []
        for con_obj in self.content:
            if issubclass(con_obj.__class__, Movie):
                out.append(con_obj)
        return out

    def get_albums(self):
        '''
        Extract all content objects that are the Album class.
        '''
        out = []
        for con_obj in self.content:
            if issubclass(con_obj.__class__, Album):
                out.append(con_obj)
        return out

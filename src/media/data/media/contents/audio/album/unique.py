#!/usr/bin/env python

#
# Copyright 2026 Chris Josephes
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
Abstract object class for the unique key.
'''
from media.data.media.contents.unique import AbstractUniqueKey
from media.general.stringtools import trans_str_ws

# pylint: disable=too-few-public-methods


class AlbumUniqueKey(AbstractUniqueKey):
    '''
    A unique identifier value.
    '''
    def __init__(self, in_album):
        super().__init__()
        self.build(in_album)

    def build(self, in_album):
        '''
        Build the unique string for the movie.
        '''
        self.c_name = in_album.__class__.__name__.casefold()
        self.title = trans_str_ws(str(in_album.title))
        a_lst = []
        if in_album.catalog:
            if in_album.catalog.copyright:
                self.year = str(in_album.catalog.copyright.year)
            if in_album.catalog.artists:
                for al in in_album.catalog.artists:
                    a_lst.append(al.sort_value)
                self.extra = '+'.join(a_lst)
        self.hash.low = self.crc32enc([self.title, self.year, self.extra])
        self.hash.high = self.crc32enc([self.extra, self.title, self.year])
        self.value = self.concat(self.title, self.year, self.hash)

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
import os
from media.general.stringtools import StringTransform
from media.general.language import LanguageHelpers

# pylint: disable=too-few-public-methods


class MovieDirPath():
    '''
    Functions used for creating a directory path.
    '''
    @staticmethod
    def build_path(in_movie):
        '''
        Main build dir path function.
        '''
        new_t = MovieDirPath._prep_string(str(in_movie.title))
        p1 = new_t[0]
        p2 = new_t[0]
        if len(new_t) > 1:
            p2 += new_t[1]
            if len(new_t) > 2:
                p2 += new_t[-1]
        path = p1 + os.sep + p2 + os.sep + str(in_movie.unique_key)
        return path

    @staticmethod
    def _prep_string(in_title_str):
        '''
        Prep function.
        '''
        tit = StringTransform.no_punc(in_title_str.casefold())
        words = tit.split()
        if len(words) > 1:
            if words[0] in LanguageHelpers.Articles_English:
                words.pop(0)
        return ''.join(words)

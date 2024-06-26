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

'''Common code related to sorting operations.'''

import string
from media.generic.language import LanguageHelpers


def transform_string(in_value):
    '''Low level change to remove all punctuation from a string.'''
    if in_value is not None:
        no_punctuation = in_value.translate(
            in_value.maketrans("", "", string.punctuation))
        return no_punctuation.casefold()
    return "SHOULDNT BE HERE"


def build_filename_string(in_value):
    '''Convert all whitespace into underscores suitable for a filename'''
    level1 = transform_string(in_value)
    return level1.translate(level1.maketrans(" \t\n\r", "____"))


def chg_ws(in_value):
    """Convert whitespace characters to underscores"""
    return in_value.translate(in_value.maketrans(" \t\n\r", "____"))


def build_sort_string(in_value):
    '''Build a string suitable for sorting, accounting for language rules.'''
    level1 = transform_string(in_value)
    word_split = level1.split()
    if word_split[0] in LanguageHelpers.Articles_English:
        article = word_split.pop(0)
        word_split.append('+'+article)
    return '_'.join(word_split)

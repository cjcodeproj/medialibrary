#!/usr/bin/env python
'''Common code related to sorting operations.'''

# pylint: disable=too-few-public-methods

import string


def transform_string(in_value):
    '''Low level change to remove all punctuation from a string.'''
    no_punctuation = in_value.translate(
             in_value.maketrans("", "", string.punctuation))
    return no_punctuation.casefold()


def build_filename_string(in_value):
    '''Convert all whitespace into underscores suitable for a filename'''
    level1 = transform_string(in_value)
    return level1.translate(level1.maketrans(" \t\n\r", "____"))


def build_sort_string(in_value):
    '''Build a string suitable for sorting, accounting for language rules.'''
    level1 = transform_string(in_value)
    word_split = level1.split()
    if word_split[0] in LanguageHelpers.Articles_English:
        article = word_split.pop(0)
        word_split.append('_'+article)
    return '_'.join(word_split)


class LanguageHelpers():
    '''Static data on languages.'''
    Articles_English = ['a', 'an', 'the']

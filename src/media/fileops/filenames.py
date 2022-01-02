#!/usr/bin/env python
'''Filename matching for the directory walker'''

# pylint: disable=too-few-public-methods

import re


class FilenameMatches():
    '''Static data on filename matches'''
    # Movie_Media = re.compile("(dvd|bluray|ultrahd|vhs)(-[\n+])?.xml$")
    Movie_Media = re.compile("-(dvd|bluray|ultrahd|vhs)(-[\\d+])?\\.xml$")
    All_Xml = re.compile("\\.xml$")

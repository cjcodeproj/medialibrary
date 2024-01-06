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

'''Common code related to manipulating titles.'''

from media.generic.stringtools import transform_string, build_sort_string
# from media.generic.language import LanguageHelpers


class TitleMunger():
    '''
    Munge title strings into usable data

    Works off of a passed title object, not a raw string.
    '''

    @classmethod
    def build_filename_string(cls, in_title):
        '''
        Build a string suitable for a filename.

        Ex: The Ugly Brige 2 becomes the_ugly_bridge_2
        '''
        level1 = transform_string(str(in_title))
        return level1.translate(level1.maketrans(" \t\n\r", "____"))

    @classmethod
    def build_sort_title_string(cls, in_title):
        '''
        Create a sortable string based on the title.

        Ex: "The Ugly Bridge 2" becomes "ugly_bridge_2_+the"
        '''
        return build_sort_string(str(in_title))

    @classmethod
    def _chk_cat_sort_title(cls, in_catalog):
        if in_catalog:
            if in_catalog.alt_titles:
                if in_catalog.alt_titles.variant_sort is True:
                    return str(in_catalog.alt_titles.variant_title)
        return None

    @classmethod
    def build_sort_cat_title(cls, in_title, in_catalog):
        '''
        Create a sortable string based in the title
        and catalog info.

        Ex: "9 Ugly Bridges" becomes "nine_ugly_bridges"
        '''
        working = TitleMunger._chk_cat_sort_title(in_catalog) or str(in_title)
        return build_sort_string(working)

    @classmethod
    def build_unique_key_string(cls, in_title, in_catalog):
        '''
        Creates a unique string for the content based on
        title and catalog info.

        Ex: "The Ugly Bridge 2" becomes "ugly_bridge_2_+the-2023-01"
        '''
        level1 = TitleMunger.build_sort_cat_title(str(in_title), in_catalog)
        year = '0000'
        idx = '1'
        if in_catalog:
            if in_catalog.copyright:
                if in_catalog.copyright.year:
                    year = str(in_catalog.copyright.year)
            if in_catalog.unique_index:
                idx = f"{in_catalog.unique_index.index:d}"
        return level1 + '-' + year + '-' + idx

    @classmethod
    def build_catalog_title(cls, in_title, in_catalog):
        '''
        Creates a title value suitable for reference notation.

        Ex: "The Ugly Bridge 2" becomes "The Ugly Bridge 2 (2023)"
        '''
        year = '0000'
        idx = 1
        if in_catalog:
            if in_catalog.copyright:
                if in_catalog.copyright.year:
                    year = str(in_catalog.copyright.year)
            if in_catalog.unique_index:
                idx = in_catalog.unique_index.index
        if idx == 1:
            return f"{in_title!s} ({year})"
        return f"{in_title!s} ({year}/{idx})"

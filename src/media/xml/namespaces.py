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

'''XML Namespace Constants'''


class Namespaces():
    '''Static data on XML Namespaces'''
    ns = {
            'media': 'http://vectortron.com/xml/media/media',
            'movie': 'http://vectortron.com/xml/media/movie',
            'audio': 'http://vectortron.com/xml/media/audio',
            'authorship': 'http://vectortron.com/xml/media/meta/authorship',
            'xml': 'http://www.w3.org/XML/1998/namespace',
            'xlink': 'http://www.w3.org/1999/xlink'
        }

    @classmethod
    def nsf(cls, in_tag):
        '''return the fully qualified namespace to the prefix format'''
        return '{' + Namespaces.ns[in_tag] + '}'

    @classmethod
    def ns_strip(cls, in_tag):
        '''Strip the namespace from an element'''
        out = in_tag.split("}", 1)
        return out[1]

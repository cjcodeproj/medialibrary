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

'''Code relating to the loading of XML files'''

# pylint: disable=too-few-public-methods

import media.xml.parser
from media.fileops.filenames import FilenameMatches


class Loader():
    '''Loads a predetermined list of media data files'''
    def __init__(self):
        self.file_count = 0
        self.object_count = 0
        self.parser = media.xml.parser.Parser()

    def load_media(self, repo, pattern=None):
        '''For each file, run the parser against it, and create an
           object if possible'''
        m_obj = []
        files = []
        if pattern is not None:
            files = repo.file_match(pattern)
        else:
            files = repo.file_match(FilenameMatches.All_Xml)
        for in_file in files:
            self.file_count += 1
            m_obj.extend(self.parser.load_file(in_file))
        self.object_count += len(m_obj)
        return m_obj

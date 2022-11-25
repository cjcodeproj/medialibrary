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

'''Main parser class for XML files'''

import xml.etree.ElementTree as ET
import xml.etree.ElementInclude as EI
import os.path
from os import chdir
import media.data.media
from media.xml.namespaces import Namespaces


class Parser():
    '''
    Main wrapper functions for all XML functionality against
    a given file.
    '''
    def __init__(self):
        self.medialist = []
        self.file_count = 0
        self.object_count = 0

    def load_file(self, in_filename):
        '''Load an XML file into the parser'''
        real_path = os.path.realpath(in_filename)
        dir_name = os.path.dirname(real_path)
        base_name = os.path.basename(real_path)
        chdir(dir_name)
        self.file_count += 1
        tree = ET.parse(base_name)
        root = tree.getroot()
        EI.include(root)
        xml_chunk = []
        for elem in root.findall('./media:media', Namespaces.ns):
            xml_chunk.append(media.data.media.Media(elem))
            self.object_count += 1
        return xml_chunk

    def stats(self):
        '''
        Report stats on how many files were read, and how many
        successful XML objects were created.
        '''
        return f"Files: {self.file_count} -- Objects {self.object_count}"

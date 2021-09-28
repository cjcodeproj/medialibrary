#!/usr/bin/env python
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

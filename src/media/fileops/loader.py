#!/usr/bin/env python

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

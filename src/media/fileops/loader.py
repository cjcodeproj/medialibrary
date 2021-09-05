#!/usr/bin/env python

'''Code relating to the loading of XML files'''

import media.xml.parser


class Loader():
    '''Loads a predetermined list of media data files'''
    def __init__(self, in_scanner):
        self.medialist = []
        self.scanner = in_scanner
        self.parser = media.xml.parser.Parser()

    def load_media(self):
        '''For each file, run the parser against it, and create an
           object if possible'''
        for in_file in self.scanner.files:
            self.medialist.extend(self.parser.load_file(in_file))

    def file_count(self):
        '''Return count on the number of files read'''
        return len(self.scanner.files)

    def object_count(self):
        '''Return count on the number of media objects created'''
        return len(self.medialist)

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

'''
Song object structure
'''

# pylint: disable=too-few-public-methods
# pylint: disable=R0801

from media.data.media.contents.genericv.technical import process_iso_duration
from media.data.media.contents.audio.elements import (
        AbstractElement, ElementTechnical
        )
from media.xml.namespaces import Namespaces


class Song(AbstractElement):
    '''
    Object representation of a song.
    '''
    def __init__(self, in_element, in_parent):
        super().__init__()
        self.catalog = None
        self.classification = None
        self.technical = None
        self.parent_o = in_parent
        self._process(in_element)

    def _process(self, in_element=None):
        super()._process(in_element)
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'technical':
                self.technical = SongTechnical(child)
        self._post_load_process()

    def _post_load_process(self):
        if not self.catalog:
            self._extract_catalog_from(self.parent_o)


class SongTechnical(ElementTechnical):
    '''
    Object representation of a song's technical data.
    '''
    def __init__(self, in_element):
        super().__init__(in_element)
        self.recording = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        super()._process(in_element)
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'studioRecording':
                self.recording = SongTechnicalRecording.STUDIO
            elif e_name == 'liveRecording':
                self.recording = SongTechnicalRecording.LIVE
            elif e_name == 'demoRecording':
                self.recording = SongTechnicalRecording.DEMO
            elif e_name == 'runtime':
                self.runtime = SongTechnicalRuntime(child)
            elif e_name == 'tempo':
                self.tempo = SongTechnicalTempo(child)


class SongTechnicalRecording():
    '''
    Identifying the type of recording for a song.
    '''
    STUDIO = 1
    LIVE = 2
    DEMO = 3

    @classmethod
    def to_string(cls, in_recording):
        '''
        Return a suitable string value.
        '''
        matrix = {
                SongTechnicalRecording.STUDIO: 'Studio Recording',
                SongTechnicalRecording.LIVE: 'Live Recording',
                SongTechnicalRecording.DEMO: 'Demo Recording'
        }
        if in_recording in matrix:
            return matrix[in_recording]
        return None


class SongTechnicalRuntime():
    '''
    Song runtime data.
    '''
    def __init__(self, in_element):
        self.overall = None
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'overall':
                dur_string = child.text
                dur_value = process_iso_duration(dur_string)
                self.overall = dur_value


class SongTechnicalTempo():
    '''
    Song tempo or bpm data.
    '''
    def __init__(self, in_element):
        self.bpm = 0
        if in_element is not None:
            self._process(in_element)

    def _process(self, in_element):
        for child in in_element:
            e_name = Namespaces.ns_strip(child.tag)
            if e_name == 'bpm':
                self.bpm = int(child.text)

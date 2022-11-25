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

'''Classes and subroutines for media display.'''

from media.data.media.medium.release import FormalType
from media.fmt.text.basics import (hdr_list,
                                   hdr_list_oneper)
from media.fmt.text.movie import MiniEntry as MovieEntry


class ListEntry():
    '''
    An entry for a piece of physical media.
    '''
    def __init__(self, in_media):
        self.media = in_media
        self.type = ''
        self.date = ''
        self.copies = 0
        self.title_key = ''
        self._prep_fields()
        if self.type:
            f_type = FormalType.formal_convert(self.type)
        else:
            f_type = 'UNKNOWN'
        self.output = f"{self.media.title!s:45.45s} {f_type:10s} " + \
                      f"{self.copies:6d} {self.date!s:s}"

    def _prep_fields(self):
        if self.media.medium.release:
            if self.media.medium.release.type:
                self.type = self.media.medium.release.type
        if self.media.library:
            if self.media.library.instances:
                self.copies = len(self.media.library.instances)
                if self.media.library.instances[0].acquisition:
                    acq = self.media.library.instances[0].acquisition
                    self.date = acq.date
        self.title_key = self.media.title.sort_title

    def __str__(self):
        return self.output

    @classmethod
    def header(cls):
        '''
        Output a report header.
        '''
        output = f"{'Title':45s} {'Media Type':10s} {'Copies':6s} " + \
                 f"{'Date':19s}\n" + \
                 f"{'-' * 45} {'-' * 10} {'-' *6} {'-' * 19}"
        return output


class BriefEntry():
    '''Formatting for a brief text record of a media device'''
    def __init__(self, in_media):
        self.media = in_media
        self._prep_fields()
        self._build_output()

    def _prep_fields(self):
        self.title_key = self.media.title.sort_title
        if self.media.medium:
            medm = self.media.medium
            if medm.release:
                self.f_type = FormalType.formal_convert(medm.release.type)
            else:
                self.f_type = 'UNKNOWN'

    def _build_output(self):
        self.output = self.entry_header()
        self.output += self.library_instances_rep()
        self.output += self.library_filing_rep()
        self.output += self.prod_id_rec()
        self.output += self.specs_inventory_rep()
        self.output += self.contents_rep()
        self.output += "\n\n"

    def entry_header(self):
        '''
        Header line for the entry.
        '''
        out = f"{self.media.title!s:60s} {self.f_type:>8s}\n" + \
              f"{'=' * 69}\n"
        return out

    def prod_id_rec(self):
        '''Product identification information.'''
        out = ''
        if self.media.medium.product_id:
            out += "Product Id > Codes\n\n"
            ids = self.media.medium.product_id
            if ids.barcodes:
                out += hdr_list_oneper('Barcode',
                                       ids.barcodes,
                                       indent=2,
                                       hformat=">8s")
            if ids.skus:
                out += hdr_list_oneper('SKU',
                                       ids.skus,
                                       indent=2,
                                       hformat=">8")
            out += "\n"
        return out

    def library_instances_rep(self, indent=2):
        '''Library information regarding copies of media.'''
        out = ''
        if self.media.library:
            lib = self.media.library
            if lib.instances:
                out += "Library > Instances\n\n"
                out += f"{' ' * indent}{'ID Label'} {'Acquisition':30s} " + \
                       f"{'Date':19s}\n" + \
                       f"{' ' * indent}{'-' * 8} {'-' *30} {'-' * 19}\n"
                for inst_i in lib.instances:
                    if not inst_i.local_id:
                        id_val = 'UNDEF'
                    else:
                        id_val = inst_i.local_id
                    if not inst_i.acquisition:
                        acq_d = 'UNKNOWN DATE'
                    else:
                        acq_d = inst_i.acquisition.date
                    out += f"{' ' * indent}{id_val:8s} " + \
                           f"{inst_i.acquisition!s:30s} " + \
                           f"{acq_d!s:19s}\n"
                out += "\n"
        return out

    def library_filing_rep(self):
        '''Library information regarding filing.'''
        out = ''
        if self.media.library:
            lib = self.media.library
            if lib.filing:
                out += "Library > Filing\n\n"
                if lib.filing.catalog:
                    fcat = lib.filing.catalog
                    out += f"    {'Catalog'}: {fcat}\n"
                if len(lib.filing.collections) > 0:
                    out += hdr_list('    Collection',
                                    lib.filing.collections)
                out += "\n\n"
        return out

    def specs_inventory_rep(self):
        '''Product Specs inventory report.'''
        out = ''
        if self.media.medium.product_specs:
            out += "Product Specs > Inventory\n\n"
            inv = self.media.medium.product_specs.inventory.inventory
            out += media_container_list(inv, padding=2)
            out += "\n"
        return out

    def contents_rep(self):
        '''Report on the contents within the media object.'''
        out = "Contents > Movies\n\n"
        out += MovieEntry.header_line()
        for con in self.media.contents:
            entry = MovieEntry(con)
            out += f"{entry!s}"
        return out

    def __str__(self):
        return self.output


def media_container_list(in_containers, padding=0):
    '''
    Take an array of containers, and then output the
    objects within them.
    '''
    padding_s = f"{' ' * padding}"
    out = padding_s
    for m_item in in_containers:
        out += media_container_object(m_item, padding=padding)
    return out


def media_container_object(in_container, padding=0, indent=0):
    '''
    Output the individual elements of a container.

    If the container contains containers, recursively
    call the function against the found container.
    '''
    padding_s = f"{' ' * padding}"
    indent_s = f"{' ' * indent}"
    label = str(in_container) + ' > '
    out = label
    subcontainers = in_container.subcontainers_list()
    media_s = in_container.media_string_count_list()
    for m_item in subcontainers:
        out += media_container_object(m_item,
                                      padding=padding,
                                      indent=len(label))
    m_count = 1
    for m_item in media_s:
        out += m_item + "\n"
        if m_count < len(media_s):
            out += f"{padding_s}{indent_s}{' ' * len(label)}"
        else:
            out += f"{padding_s}{indent_s}"
        m_count += 1
    return out

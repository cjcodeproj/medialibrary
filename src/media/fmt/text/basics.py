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

'''
Formatting functions for basic plain text output.
'''

import textwrap


DEF_WIDTH = 76


def hdr_list(header, i_list):
    '''
    Output a list of items with a header
    '''
    out_string = ""
    if len(i_list) == 1:
        out_string = f"{header}: {i_list[0]}"
    else:
        hdr_string = f"{header}s: "
        bfr_string = " " * len(hdr_string)
        str_list = ""
        for i_name in i_list:
            str_list += f"{i_name}, "
        str_list = str_list[:-2]
        out_ar = textwrap.wrap(str_list, width=DEF_WIDTH,
                               initial_indent=hdr_string,
                               subsequent_indent=bfr_string)
        out_string = "\n".join(out_ar)
    return out_string


def hdr_block(header, i_list):
    '''
    Output a larger list of items with a header
    '''
    out_string = ""
    if len(i_list) == 1:
        out_string = f"{header}:\n{i_list[0]}"
    else:
        hdr_string = f"{header}s:"
        str_list = ""
        for i_name in i_list:
            str_list += f"{i_name}, "
        str_list = str_list[:-2]
        out_ar = textwrap.wrap(str_list, width=DEF_WIDTH,
                               initial_indent=' ',
                               subsequent_indent=' ')
        out_string = hdr_string + "\n" + "\n".join(out_ar)
    return out_string


def hdr_list_np(header, i_list):
    '''
    Output a larger list of items with a header,
    but no pluralization of the header based on
    item count.
    '''
    out_string = ""
    hdr_string = f"{header}: "
    bfr_string = " " * len(hdr_string)
    str_list = ""
    for i_name in i_list:
        str_list += f"{i_name}, "
    str_list = str_list[:-2]
    out_ar = textwrap.wrap(str_list, width=DEF_WIDTH,
                           initial_indent=hdr_string,
                           subsequent_indent=bfr_string)
    out_string = "\n".join(out_ar) + "\n"
    return out_string


def hdr_text(header, text_block):
    '''
    Output a block of text
    '''
    out_string = header + "\n"
    out_ar = textwrap.wrap(text_block, width=DEF_WIDTH)
    out_string += "\n".join(out_ar)
    return out_string


def hdr_list_oneper(header, i_list, indent=0, hformat='s'):
    '''
    Output a list with a header, one item per line.

    header: item1
            item2

    allow for an indent option to pad all output
    and a format specifier if multiple runs of
    hdr_list_oneper need to be aligned at the colon.
    '''
    out = ""
    if len(i_list) == 1:
        f_header = f"{' ' * indent}{header:{hformat}}"
        out = f"{f_header}: {i_list[0]}\n"
    else:
        f_header = f"{' ' * indent}{(header + 's'):{hformat}}"
        bfr_string = " " * len(f_header)
        i_count = 1
        for i_name in i_list:
            if i_count == 1:
                out += f"{f_header}: {i_name}\n"
            else:
                out += f"{bfr_string}  {i_name}\n"
            i_count += 1
    return out

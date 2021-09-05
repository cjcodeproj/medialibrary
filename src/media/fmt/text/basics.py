#!/usr/bin/env python
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
        out_string = "{0}: {1}".format(header, i_list[0])
    else:
        hdr_string = "{0}s: ".format(header)
        bfr_string = " " * len(hdr_string)
        str_list = ""
        for i_name in i_list:
            str_list += "{0}, ".format(i_name)
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
        out_string = "{0}:\n{1}".format(header, i_list[0])
    else:
        hdr_string = "{0}s:".format(header)
        str_list = ""
        for i_name in i_list:
            str_list += "{0}, ".format(i_name)
        str_list = str_list[:-2]
        out_ar = textwrap.wrap(str_list, width=DEF_WIDTH,
                               initial_indent=' ',
                               subsequent_indent=' ')
        out_string = hdr_string + "\n" + "\n".join(out_ar)
    return out_string


def hdr_text(header, text_block):
    '''
    Output a block of text
    '''
    out_string = header + "\n"
    out_ar = textwrap.wrap(text_block, width=DEF_WIDTH)
    out_string += "\n".join(out_ar)
    return out_string
